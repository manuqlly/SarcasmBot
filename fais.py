from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings  # ✅ Use local embeddings
import asyncpg
import asyncio
from tqdm.asyncio import tqdm  

DATABASE_URL = "postgresql://postgres:root@localhost/discord_bot" #use your DB ADDRESS
BATCH_SIZE = 100

# ✅ Load SentenceTransformer embeddings (FREE, no API calls!)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

async def fetch_messages():
    """Fetch messages from PostgreSQL."""
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("SELECT content FROM discord_messages")
    await conn.close()
    return [row['content'] for row in rows]

async def store_embeddings():
    """Fetch messages and store embeddings in FAISS with batching."""
    print("🔄 Fetching messages from database...")
    docs = await fetch_messages()

    if not docs:
        print("⚠️ No messages found in the database.")
        return

    print(f"✅ Fetched {len(docs)} messages. Processing in batches of {BATCH_SIZE}...")

    vector_store = None  # Initialize FAISS store

    for i in tqdm(range(0, len(docs), BATCH_SIZE), desc="Processing Batches"):
        batch = docs[i : i + BATCH_SIZE]
        print(f"🚀 Processing batch {i // BATCH_SIZE + 1}/{len(docs) // BATCH_SIZE + 1}...")

        try:
            batch_embeddings = FAISS.from_texts(batch, embeddings)
            
            if vector_store is None:
                vector_store = batch_embeddings  # Initialize FAISS store
            else:
                vector_store.merge_from(batch_embeddings)  # Merge batches

        except Exception as e:
            print(f"❌ Error processing batch {i // BATCH_SIZE + 1}: {e}")
            continue  # Skip to next batch

    if vector_store:
        print("💾 Saving FAISS index...")
        vector_store.save_local("faiss_index")
        print("✅ FAISS index saved!")

async def main():
    await store_embeddings()

# Run the async function
asyncio.run(main())
