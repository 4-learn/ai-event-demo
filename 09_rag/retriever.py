import re

from sentence_transformers import SentenceTransformer


class Retriever:
    def __init__(self, regulations):
        self.regulations = regulations
        self.model = SentenceTransformer("intfloat/multilingual-e5-small", device="cpu")
        chunks = []
        self.owners = []
        for index, rule in enumerate(regulations):
            for sentence in re.split(r"(?<=[。；])", rule["text"]):
                if sentence.strip():
                    chunks.append("passage: " + rule["section"] + "\n" + sentence)
                    self.owners.append(index)
        self.vectors = self.model.encode(chunks, normalize_embeddings=True)

    def search(self, question, top_k=3):
        vector = self.model.encode("query: " + question, normalize_embeddings=True)
        chunk_scores = self.vectors @ vector
        scores = [
            float(max(chunk_scores[j] for j, owner in enumerate(self.owners) if owner == i))
            for i in range(len(self.regulations))
        ]
        indexes = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        # 用短句找出相關位置，但回傳完整條文，避免丟掉限制與前後文。
        return [{**self.regulations[i], "score": scores[i]} for i in indexes]
