import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))

from answer_check import check_answer
from llm import answer_question
from retriever import Retriever

parser = argparse.ArgumentParser(description="固定題目 RAG 測試；每題呼叫 API 一次，不自動重試")
parser.add_argument("--questions", type=Path, default=ROOT / "questions.json")
parser.add_argument("--output", type=Path, default=ROOT / "generation_results.json")
args = parser.parse_args()
regulations = json.loads((ROOT.parent.parent / "08_crawler" / "regulations.json").read_text())
cases = json.loads(args.questions.read_text())
retriever = Retriever(regulations)
report = {
    "model": os.getenv("LLM_MODEL", "gpt-6-luna"),
    "tested_at": datetime.now(timezone.utc).isoformat(),
    "retriever": "multilingual-e5-small, sentence index, full-article return, top-3",
    "reasoning_effort": "none",
    "temperature": 0,
    "prompt": (ROOT.parent / "prompt.txt").read_text(encoding="utf-8"),
    "results": [],
}

for case in cases:
    start = time.monotonic()
    evidence = retriever.search(case["question"])
    ids = [rule["id"] for rule in evidence]
    row = {
        **case,
        "retrieved": ids,
        "evidence": evidence,
        "retrieval_pass": set(case["required"]).issubset(ids) if case["required"] else None,
    }
    try:
        answer, usage, response_id = answer_question(case["question"], evidence)
        row.update(answer=answer, usage=usage, response_id=response_id)
        try:
            check_answer(answer, evidence)
            row["citation_check"] = "pass"
        except ValueError as error:
            row["citation_check"] = str(error)
        # 此處不以關鍵字宣稱語意正確；答案逐題逐題核對。
        row["semantic_review"] = "pending"
    except Exception as error:
        row["error"] = str(error)
    row["elapsed_seconds"] = round(time.monotonic() - start, 2)
    report["results"].append(row)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(case["id"], row.get("citation_check", row.get("error")), row.get("answer", {}).get("status"), flush=True)
    if "error" in row:
        print("停止測試，先檢查 API／輸出錯誤，不繼續付費呼叫。", flush=True)
        break
