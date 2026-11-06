import math
import re
from collections import Counter


def tokens(text):
    text = re.sub(r"\s+", "", text.lower())
    return Counter(text[i:i + 2] for i in range(len(text) - 1))


def retrieve(question, regulations, top_k=3):
    documents = [tokens(rule["section"] + rule["text"]) for rule in regulations]
    question_tokens = tokens(question)
    vocabulary = set().union(*documents)
    idf = {
        word: math.log((len(documents) + 1) / (1 + sum(word in doc for doc in documents))) + 1
        for word in vocabulary
    }

    def score(doc):
        dot = sum(question_tokens[w] * doc[w] * idf[w] ** 2 for w in question_tokens.keys() & doc.keys())
        qnorm = math.sqrt(sum((count * idf.get(w, 1)) ** 2 for w, count in question_tokens.items()))
        dnorm = math.sqrt(sum((count * idf[w]) ** 2 for w, count in doc.items()))
        return dot / (qnorm * dnorm) if qnorm * dnorm else 0

    ranked = sorted(zip(regulations, documents), key=lambda item: score(item[1]), reverse=True)
    return [{**rule, "score": round(score(doc), 4)} for rule, doc in ranked[:top_k] if score(doc) > 0]
