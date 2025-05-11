from typing import List, Dict, Any
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from rag_stack.prompt_templates import QnA_prompt
from langchain_anthropic import ChatAnthropic

class QueryProcessor:
    """
    Processes user queries and retrieves relevant information
    """
    def __init__(self, persist_directory: str = None, llm: str = 'openai'):
        self.persist_directory = persist_directory or os.getenv('VECTOR_DB_PATH') or "./vector_db"

        if llm == "openai":
            self.model_name = os.getenv('OPENAI_EMBEDDING_MODEL') or "text-embedding-ada-002"
            self.embedding_model = OpenAIEmbeddings(model=self.model_name)
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    
    async def retreive_context(self, user_query: str, top_k: int):
        try:
            load_vector_store = FAISS.load_local(self.persist_directory, self.embedding_model, allow_dangerous_deserialization=True)
            retrieved_docs = load_vector_store.similarity_search(user_query, top_k)
            # retrieved_docs = load_vector_store.similarity_search_with_relevance_scores(user_query, top_k)
            return retrieved_docs
        except Exception as e:
            print('➡ Error in retreive_context:', e)
            raise e
        
    async def generate_response(self, query: str, context, llm: str):
        """ Generate a response using LLM based on user query and context """
        prompt = ChatPromptTemplate.from_messages(QnA_prompt)

        if llm == "openai": 
            llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        elif llm == "claude":
            llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.2)

        chain = prompt | llm
        llm_response = await chain.ainvoke({
            "question": query,
            "context": context
        })

        return llm_response.content
