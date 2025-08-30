import tempfile
import os
from typing import List, Optional
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document


class PDFProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def process_uploaded_file(self, uploaded_file) -> List[Document]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        
        try:
            documents = self.load_and_split(tmp_path)
            return documents
        finally:
            os.unlink(tmp_path)
    
    def load_and_split(self, file_path: str) -> List[Document]:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return self.text_splitter.split_documents(documents)
    
    def extract_text_from_documents(self, documents: List[Document]) -> str:
        return "\n".join([doc.page_content for doc in documents])
    
    def validate_pdf(self, file_path: str) -> bool:
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            return len(documents) > 0 and any(doc.page_content.strip() for doc in documents)
        except Exception:
            return False