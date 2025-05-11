import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

class VectorStore:
    """
    Manages storage and retrieval of vector embeddings
    """
    def __init__(self, persist_directory: str = None, llm: str = "openai"):
        self.persist_directory = persist_directory or os.getenv('VECTOR_DB_PATH') or "./vector_db"
        os.makedirs(self.persist_directory, exist_ok=True)

        if llm == "openai":
            self.model_name = os.getenv('OPENAI_EMBEDDING_MODEL') or "text-embedding-ada-002"
            self.embedding_model = OpenAIEmbeddings(model=self.model_name)
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        if llm == "claude":
            self.model_name = os.getenv('CLAUDE_EMBEDDING_MODEL') or "voyage-3"
            self.embedding_model = ""
            self.llm = ""
    
    async def add_embeddings_to_vector_store(self, text_chunks: list):
        try:
            texts = [chunk.page_content for chunk in text_chunks]  # Extract text/page content from the chunks
            vector_store = FAISS.from_texts(texts, embedding=self.embedding_model)

            # save it to the local index
            vector_store.save_local(os.getenv('VECTOR_DB_PATH'))
            print(f"Stored to the local disk at: '{os.getenv('VECTOR_DB_PATH')}'")
            return True
        except Exception as e:
            print('➡ Error in add_embeddings_to_vector_store:', e)
            raise e
