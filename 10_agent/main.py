from agent import run_agent

question = input("想了解什麼？ ") or "請回顧七天模擬事件，指出優先改善的區域，並查規範提出兩項建議。"
report = run_agent(question)

print("\n", report["summary"])
for item in report["recommendations"]:
    print(item["zone"], item["action"], item["rule_id"])
