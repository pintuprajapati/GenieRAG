import os
import pymupdf4llm
import pathlib
import time
import utils
import config
from rag_stack.models import DocumentType

class DocumentProcessor:
    """
    Handles document text extraction
    """
    
    def __init__(self):
        os.makedirs(config.MD_FILES_DIR, exist_ok=True)
        self.file_name = ""
        self.file_extension = ""

    async def extract_text(self, file_path: str) -> str:
        """Extract text from various document types"""

        self.file_name = file_path.split("/")[-1] # extract filename.ext
        self.file_extension = self.file_name.split(".")[-1] # split 'filename' and 'ext'

        if self.file_extension == DocumentType.PDF:
            filepath = await self._extract_from_pdf(file_path)
            return filepath
        else:
            raise ValueError(f"Unsupported document type: {self.file_extension}")
    
    async def extract_using_pymupdf(self, file_path: str) -> str:
        """ Extract the data into markdown format (including tables, multi-columns and indexes) """
        
        print(f"Started extracting text using PyMuPDF (In Progress)...")
        start_time = time.time()
        md_text = pymupdf4llm.to_markdown(file_path)
        print(f"Extraction completed.")
        print(f"Total time taken for extracting text from pdf: {time.time() - start_time}")
        
        static_file_dir = os.path.join(config.MD_FILES_DIR)
        utils.create_local_dir(static_file_dir)
        
        # Create file path
        ext = f"{self.file_name.split('.')[0]}.md"
        md_filepath = os.path.join(static_file_dir, ext)
        
        # Save extracted text to a md file
        pathlib.Path(md_filepath).write_bytes(md_text.encode())
        return md_filepath
    
    async def _extract_from_pdf(self, file_path: str) -> str:
        return await self.extract_using_pymupdf(file_path)
    