from agent import run_agent
from report import save_report

question = input("想了解什麼？ ") or "請回顧七天模擬事件，指出優先改善的區域，並查規範提出兩項建議。"
report = run_agent(question)
pdf_path = save_report(report)

print("\n", report["summary"])
print("PDF 已產生：", pdf_path)
