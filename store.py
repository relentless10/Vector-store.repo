import json
from similarity import cosine_similarity


class VectorStore:
    def __init__(self):
        self.vectors = {}
        self.metadata = {}

    def add(self, id, vector, text=None):
        if id in self.vectors:
            raise ValueError(f"ID {id} already exists")
        self.vectors[id] = vector
        self.metadata[id] = {"text": text}

    def get(self, id):
        if id not in self.vectors:
            return None
        return {
            "id": id,
            "vector": self.vectors[id],
            "text": self.metadata[id]["text"]
        }

    def delete(self, id):
        if id not in self.vectors:
            return False
        del self.vectors[id]
        del self.metadata[id]
        return True

    def update(self, id, vector=None, text=None):
        if id not in self.vectors:
            return False
        if vector is not None:
            self.vectors[id] = vector
        if text is not None:
            self.metadata[id]["text"] = text
        return True

    def search(self, query_vector, top_k=5):
        results = []
        for id, vector in self.vectors.items():
            score = cosine_similarity(query_vector, vector)
            results.append({
                "id": id,
                "score": score,
                "text": self.metadata[id]["text"]
            })
        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]

    def save_to_file(self, filepath):
        data = {
            "vectors": self.vectors,
            "metadata": self.metadata
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load_from_file(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        self.vectors = data["vectors"]
        self.metadata = data["metadata"]


if __name__ == "__main__":
    store = VectorStore()
    store.add("1", [1, 0, 0], "cat")
    store.add("2", [0, 1, 0], "dog")
    store.add("3", [1, 0.1, 0], "kitten toy")

    assert store.get("1")["text"] == "cat"

    store.update("1", text="kitten")
    assert store.get("1")["text"] == "kitten"

    top_matches = store.search([1, 0, 0], top_k=2)
    print("Search results:", top_matches)

    assert store.delete("1") == True
    assert store.get("1") is None

    store.save_to_file("test_store.json")
    new_store = VectorStore()
    new_store.load_from_file("test_store.json")
    assert new_store.get("2")["text"] == "dog"

    print("All tests passed ✅")

