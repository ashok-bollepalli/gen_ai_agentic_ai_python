import os
from infrastructure.config import DATA_FOLDER

def load_documents():
    """Read every TXT file from the data folder."""
    documents = []

    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_FOLDER, filename)

            with open(path, "r", encoding="utf-8") as file:
                documents.append({
                    "source": filename,
                    "text": file.read()
                })

    return documents
