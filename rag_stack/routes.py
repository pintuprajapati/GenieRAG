from fastapi import APIRouter, UploadFile, File
from typing import Dict, Any
import shutil
import os
import config
from utils import create_local_dir, create_response
from rag_stack.document_processing import DocumentProcessor
from rag_stack.chunking import TextChunker
from rag_stack.vector_storage import VectorStore
from rag_stack.query import QueryProcessor

document_processor = DocumentProcessor()
document_chunker = TextChunker()
vector_store = VectorStore()
query_processor = QueryProcessor()

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/documents/ingest", response_model=Dict[str, Any])
async def upload_document(file: UploadFile = File(...)):
    """
    Ingest a document for processing
    Handles storing file into local dir, extract text data, create Document chunks, Embed adn store them into vector db
    """
    try:
        document_info = {}
        upload_dir = os.path.join(config.STATIC_DIR, 'uploaded_files')        
        create_local_dir(upload_dir)
        
        filename = file.filename
        # file_extension = file.filename.split(".")[-1].lower()
        
        file_path = os.path.join(upload_dir, f"{filename}")
        print('➡ Uploaded file_path:', file_path)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        document_info['upload_status'] = f"File uploaded successfully"

        extracted_fileath = await document_processor.extract_text(file_path)
        # for testing purpose
        # extracted_fileath = "static/md_files/Minimalism by Mil Hoornaert - chapter1.md"
        print('➡ extracted_file_path:', extracted_fileath)
        document_info['extracted_filepath'] = "Texts have been extracted from file(s)"

        chunk_docs = await document_chunker.chunk_text(extracted_fileath)
        document_info['chunk_status'] = "Extracted texts have been chunked successfully"

        vector_status = await vector_store.add_embeddings_to_vector_store(chunk_docs)
        if vector_status:
            document_info['vector_status'] = "Chunks have been stored to the vector db"

        return create_response(message="Document has been processed.", status_code=200, success=True, data=document_info)
    except Exception as e:
        return create_response(message="Something went wrong while uploading a document", status_code=500, success=False, data={})

@router.get("/query",  response_model=Dict[str, Any])
async def query_documents(query: str, top_k: int = 5, llm: str = "openai"):
    """Query the document database"""
    try:
        get_relevant_docs = await query_processor.retreive_context(query, top_k)
        response = await query_processor.generate_response(query, get_relevant_docs, llm)
        
        result_data = {
            "query": query,
            "llm_used": llm,
            "llm_response": response,
            "context": get_relevant_docs
        } 
        
        return create_response(message="Result fetched successfully", status_code=200, success=True, data=result_data)
    except Exception as e:
        print("➡ Error in query_documents: ", e)
        return create_response(message="Something went wrong while getting answer for the query:", status_code=500, success=False, data={str(e)})