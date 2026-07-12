def cosine_similarity(vector1, vector2):
    """
    Measures how similar two vectors are, based on direction (not size).
    Returns a score from -1 (opposite) to 1 (identical).
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be the same length")

    # Step 1: dot product - multiply matching positions, sum them up
    dot_product = sum(a * b for a, b in zip(vector1, vector2))

    # Step 2: magnitude (length) of each vector
    magnitude1 = sum(a ** 2 for a in vector1) ** 0.5
    magnitude2 = sum(b ** 2 for b in vector2) ** 0.5

    # Step 3: avoid dividing by zero (empty/zero vector edge case)
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    # Step 4: cosine similarity formula
    return dot_product / (magnitude1 * magnitude2)


# Manual tests
if __name__ == "__main__":
    assert cosine_similarity([1, 0, 0], [1, 0, 0]) == 1.0
    assert round(cosine_similarity([1, 0, 0], [0, 1, 0]), 5) == 0.0
    assert round(cosine_similarity([1, 1], [1, 1]), 5) == 1.0
    print("All similarity tests passed ✅")
