
def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into overlapping chunks of approximately chunk_size characters.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        if end == len(text):
            break
        start += chunk_size - overlap
    return chunks
