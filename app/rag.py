import os
from chromadb import PersistentClient
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#chroma_client = PersistentClient(path=os.getenv('PERSIST_DIR'))

class Retriever:
    def __init__(self, collection_name="mental_health_counseling"):
        self.client = PersistentClient(path=os.getenv('PERSIST_DIR'))
        self.collection = self.client.get_or_create_collection(collection_name)
        #self.enc = encoding_for_model(os.getenv("EMBED_MODEL"))

    #def add(self, ids, texts):                              # one‑time ingest
    #    embs = openai.Embedding.create(input=texts,
    #                                   model=os.getenv("EMBED_MODEL"))["data"]
    #    self.col.add(documents=texts, embeddings=[e["embedding"] for e in embs],
    #                 ids=ids)

    def get(self, query, k=3):
        query_embeddings = openai_client.embeddings.create(
            input=query,
            model=os.getenv("EMBEDDING_MODEL")
            ).data[0].embedding
        similar_docs = self.collection.query(
            query_embeddings=[query_embeddings], 
            n_results=k
            )
        return similar_docs["documents"][0] 
