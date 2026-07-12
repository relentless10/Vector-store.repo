import sqlite3
import json
from similarity import cosine_similarity


class SQLiteVectorStore:
    def __init__(self, db_path="vectors.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                id TEXT PRIMARY KEY,
                vector TEXT NOT NULL,
                text TEXT
            )
        """)
        self.conn.commit()

    def add(self, id, vector, text=None):
        existing = self.conn.execute(
            "SELECT id FROM vectors WHERE id = ?", (id,)
        ).fetchone()
        if existing:
            raise ValueError(f"ID {id} already exists")
        self.conn.execute(
            "INSERT INTO vectors (id, vector, text) VALUES (?, ?, ?)",
            (id, json.dumps(vector), text)
        )
        self.conn.commit()

    def get(self, id):
        row = self.conn.execute(
            "SELECT id, vector, text FROM vectors WHERE id = ?", (id,)
        ).fetchone()
        if row is None:
            return None
        return {"id": row[0], "vector": json.loads(row[1]), "text": row[2]}

    def delete(self, id):
        cursor = self.conn.execute("DELETE FROM vectors WHERE id = ?", (id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def update(self, id, vector=None, text=None):
        existing = self.get(id)
        if existing is None:
            return False
        new_vector = vector if vector is not None else existing["vector"]
        new_text = text if text is not None else existing["text"]
        self.conn.execute(
            "UPDATE vectors SET vector = ?, text = ? WHERE id = ?",
            (json.dumps(new_vector), new_text, id)
        )
        self.conn.commit()
        return True

    def search(self, query_vector, top_k=5):
        rows = self.conn.execute("SELECT id, vector, text FROM vectors").fetchall()
        results = []
        for id, vector_json, text in rows:
            vector = json.loads(vector_json)
            score = cosine_similarity(query_vector, vector)
            results.append({"id": id, "score": score, "text": text})
        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]


if __name__ == "__main__":
    store = SQLiteVectorStore("test_vectors.db")

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

    print("All SQLite tests passed ✅")