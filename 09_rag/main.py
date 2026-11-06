import json
from pathlib import Path

from retriever import Retriever
from llm import answer_question
from answer_check import check_answer

ROOT = Path(__file__).parent
regulations = json.loads(
    (ROOT.parent / "08_crawler" / "regulations.json").read_text(encoding="utf-8")
)
retriever = Retriever(regulations)

question = input("想查詢什麼規範？ ")
evidence = retriever.search(question)

answer, usage, response_id = answer_question(question, evidence)
check_answer(answer, evidence)
print(answer["answer"])

for citation in answer["citations"]:
    rule = next(rule for rule in evidence if rule["id"] == citation["id"])
    print(rule["section"], rule["source"])
    print("原文：", citation["quote"])

print("Token 用量：", usage["total_tokens"])
