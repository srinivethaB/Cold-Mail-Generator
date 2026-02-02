import os
import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path=None):
        # Fix CSV path: build path relative to this file
        if file_path is None:
            base_dir = os.path.dirname(__file__)  # folder where portfolio.py is
            file_path = os.path.join(base_dir, "resource", "my_portfolio.csv")
        self.file_path = file_path

        # Load CSV
        self.data = pd.read_csv(file_path)

        # Initialize Chroma client
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
