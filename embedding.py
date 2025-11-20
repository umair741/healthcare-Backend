import os
import asyncio
from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from doctor_processing import fetch_doctors_data  

PERSIST_DIR = "chroma_db"
os.makedirs(PERSIST_DIR, exist_ok=True)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

async def create_doctors_embeddings(batch_size=32):
    doctors_texts = await fetch_doctors_data()
    if not doctors_texts:
        return [], []
    embeddings = await asyncio.to_thread( model.encode, doctors_texts, batch_size=batch_size, show_progress_bar=False)
    embeddings_list = embeddings.tolist()  

    return doctors_texts, embeddings_list

def store_in_chroma(doctors_texts, embeddings_list):

    if not doctors_texts or not embeddings_list:
        print("No data to store in ChromaDB.")
        return
    vectorstore = Chroma(
        collection_name="doctors",
        persist_directory=PERSIST_DIR
    )
    vectorstore.add_texts(
        texts=doctors_texts,
        embeddings=embeddings_list,
        metadatas=[{"doctor_index": i} for i in range(len(doctors_texts))],
        ids=[f"doc_{i}" for i in range(len(doctors_texts))]
    )

    print(f"{len(doctors_texts)} doctor embeddings stored in ChromaDB!")

async def main():
    doctors_texts, embeddings_list = await create_doctors_embeddings()
    if embeddings_list:
        print(f"Generated {len(embeddings_list)} embeddings. Each embedding length: {len(embeddings_list[0])}")
        store_in_chroma(doctors_texts, embeddings_list)
    else:
        print("No embeddings generated.")

# ----------------------------
if __name__ == "__main__":
    asyncio.run(main())
