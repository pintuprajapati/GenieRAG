import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_experimental.text_splitter import SemanticChunker
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class TextChunker:
    """
    Handles text chunking and metadata enrichment for document processing.
    """
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or os.getenv('CHUNK_SIZE')
        self.chunk_overlap = chunk_overlap or os.getenv('CHUNK_OVERLAP')

        self.embedding_model = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
        self.openai_llm = ChatOpenAI(model="gpt-4o", temperature=0.4)

        self.semantic_text_splitter = SemanticChunker(
            embeddings=self.embedding_model,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=0.98
        )
    
    async def chunk_text(self, extracted_filepath: str):
        """
        Chunk the document using Langchain
        """
        try:
            with open(extracted_filepath, "r", encoding="utf-8") as f:
                content = f.read()

            return await self.recursive_char_txt_splitter(content)
            # await self.semantic_chunking_by_langchain(documents)

        except Exception as e:
            print('➡ error in chunk_text: ', e)
            raise e

    async def recursive_char_txt_splitter(self, content: str):
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=400,
                chunk_overlap=50,
                length_function=len,
                is_separator_regex=False
            )

            # creating a langchain Document
            langchain_docs = text_splitter.create_documents([content])
            split_docs = text_splitter.split_documents(langchain_docs)

            return split_docs
        except Exception as e:
            print('➡ Error in recursive_char_txt_splitter:', e)
            raise e
    
    async def semantic_chunking_by_langchain(self, content: str):
        try:
            ...
        except Exception as e:
            print('➡ Error in semantic_chunking_by_langchain:', e)
            raise e

