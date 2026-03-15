import openai
from dotenv import load_dotenv
import os
from typing import List
from langchain_core.documents import Document
from config.db_config import Db_config

load_dotenv()

db = Db_config()

class Ingest:

    def __init__(self) -> None:
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
        self.OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

    def initialize_db(self): 
        conn = db.get_db_connection()

        with conn.cursor() as cur:

            cur.execute("""
            CREATE EXTENSION IF NOT EXISTS vector;
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector(1536),
                doc_name TEXT
            );
            """)

        conn.commit()
        conn.close()

    def load_document(self, doc_name) -> Document:
        print("load docs")
        file_dir = os.path.dirname(os.path.abspath(__file__))
        md_files = os.path.join(file_dir + "/assets/", doc_name)

        document = None

        if os.path.exists(md_files):
            with open(md_files, "r", encoding="utf-8") as fh:
                text = fh.read().strip()

                if text:
                    doc = Document(
                            page_content=text,
                            metadata={"source": doc_name}
                        )
                    document = doc

        return document
    
    def sliding_window_chunking(self, document, chunk_size, overlap):
        chunks = []
        doc_content = document.page_content
        for i in range(0, len(doc_content), chunk_size - overlap):
            chunk = doc_content[i:i+chunk_size]
            chunks.append(chunk)
        return chunks
    
    def create_chunks(self, document):
        print("creating chunks...")
        chunks = self.sliding_window_chunking(document=document, 
                                              chunk_size=100, 
                                              overlap=20)
        return chunks
    
    def store_in_vectordb(self, chunks, doc_name) -> bool:
        try:
            print("converting document chunks in embeddings...")
            client = openai.OpenAI(api_key=self.OPEN_API_KEY)
            response = client.embeddings.create(model=self.EMBEDDING_MODEL, 
                                    input=chunks)

            conn = db.get_db_connection()

            for i in range(0, len(response.data)):
                # retrieve embeddings & store them
                embedding = response.data[i].embedding
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO documents (content, embedding, doc_name) VALUES (%s, %s, %s)",
                                (chunks[i], embedding, doc_name))

            conn.commit()
            conn.close()
            print("embeddings stored & vector DB...")
            return True
        except Exception as e:
             print("Error while creating vector embeddings and storing in DB...", e)
             return False
        
    def ingest_document(self):
        try:
            self.initialize_db()

            doc_arr = ["investment.md", "equity_stocks_investment.md"]
            document: Document
            for i in range(0, len(doc_arr)):
                doc_name = doc_arr[i]
                print(f"initiating process for {doc_name}")
                document = self.load_document(doc_name)
                
                chunks = self.create_chunks(document=document)
                result = self.store_in_vectordb(chunks=chunks, doc_name=doc_name)
                if result:
                    print(f"Embeddings created successfully for document: {doc_name}")
                else:
                    print(f"Error occured while embedding document {doc_name} for RAG")

                document = None
        except Exception as e:        
            return {
                "status": "failed",
                "exception": e.__cause__()
            }
        
        return {
            "status": "success"
        }


if __name__ == "__main__":
    # Get strategy from command line argument
    ingest = Ingest()
    ingest.initialize_db()

    doc_arr = ["investment.md", "equity_stocks_investment.md"]
    document: Document
    for i in range(0, len(doc_arr)):
        doc_name = doc_arr[i]
        print(f"initiating process for {doc_name}")
        document = ingest.load_document(doc_name)
        
        chunks = ingest.create_chunks(document=document)
        result = ingest.store_in_vectordb(chunks=chunks, doc_name=doc_name)
        if result:
            print(f"Embeddings created successfully for document: {doc_name}")
        else:
            print(f"Error occured while embedding document {doc_name} for RAG")

        document = None

    