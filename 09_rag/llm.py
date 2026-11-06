import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT.parent / "config.env")


def answer_question(question, evidence):
    token = os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("請先在 config.env 設定 OPENAI_API_KEY")

    schema = {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["answered", "insufficient"]},
            "answer": {"type": "string"},
            "citations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "enum": [r["id"] for r in evidence]},
                        "quote": {"type": "string"},
                    },
                    "required": ["id", "quote"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["status", "answer", "citations"],
        "additionalProperties": False,
    }
    context = [{key: rule[key] for key in ("id", "section", "text")} for rule in evidence]
    payload = {
        "model": os.getenv("LLM_MODEL", "gpt-6-luna"),
        "instructions": (ROOT / "prompt.txt").read_text(encoding="utf-8"),
        "input": json.dumps({"question": question, "evidence": context}, ensure_ascii=False),
        "reasoning": {"effort": "none"},
        "temperature": 0,
        "max_output_tokens": 900,
        "store": False,
        "text": {"format": {"type": "json_schema", "name": "policy_answer", "strict": True, "schema": schema}},
    }
    request = Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=45) as response:
            result = json.load(response)
    except HTTPError as error:
        # 不輸出請求或金鑰；不自動重試，避免額外費用。
        body = json.loads(error.read())
        code = body.get("error", {}).get("code")
        raise RuntimeError(f"OpenAI API HTTP {error.code}，錯誤代碼：{code}") from None

    if result.get("status") != "completed":
        raise ValueError("模型未完成回答，請查看用量與輸出上限")
    text = "".join(
        content["text"]
        for item in result["output"] if item.get("type") == "message"
        for content in item["content"] if content.get("type") == "output_text"
    )
    return json.loads(text), result["usage"], result["id"]
