def check_answer(result, evidence):
    """檢查格式與引用原文；不保證原文在語意上支持答案。"""
    if result.get("status") not in ("answered", "insufficient"):
        raise ValueError("回答狀態不正確")
    if not isinstance(result.get("answer"), str) or not result["answer"].strip():
        raise ValueError("回答不可空白")
    citations = result.get("citations")
    if not isinstance(citations, list):
        raise ValueError("引用格式不正確")
    if result["status"] == "answered" and not citations:
        raise ValueError("回答缺少引用")

    available = {rule["id"]: rule for rule in evidence}
    for citation in citations:
        if not isinstance(citation, dict):
            raise ValueError("引用格式不正確")
        rule = available.get(citation.get("id"))
        quote = citation.get("quote")
        if rule is None or not isinstance(quote, str) or not quote.strip():
            raise ValueError("引用不在本次檢索的證據中")
        if quote not in rule["text"]:
            raise ValueError("引用原文與文件不符")
    return result
