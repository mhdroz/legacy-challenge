import os
from chromadb import PersistentClient
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

openai_api_key = st.secrets["api"]["OPENAI_API_KEY"]
load_dotenv()


openai_client = OpenAI(api_key=openai_api_key)

#chroma_client = PersistentClient(path=os.getenv('PERSIST_DIR'))

class Retriever:
    def __init__(self, collection_name="mental_health_counseling"):
        self.client = PersistentClient(path=os.getenv('PERSIST_DIR'))
        self.collection = self.client.get_or_create_collection(collection_name)

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
