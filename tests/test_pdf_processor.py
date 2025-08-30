import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from src.utils.pdf_processor import PDFProcessor


class TestPDFProcessor:
    def setup_method(self):
        self.processor = PDFProcessor(chunk_size=500, chunk_overlap=50)
    
    def test_initialization(self):
        assert self.processor.chunk_size == 500
        assert self.processor.chunk_overlap == 50
        assert self.processor.text_splitter.chunk_size == 500
        assert self.processor.text_splitter.chunk_overlap == 50
    
    @patch('src.utils.pdf_processor.PyPDFLoader')
    def test_load_and_split_success(self, mock_loader):
        mock_doc = Mock()
        mock_doc.page_content = "Sample document content"
        mock_loader.return_value.load.return_value = [mock_doc]
        
        result = self.processor.load_and_split("dummy_path.pdf")
        
        assert len(result) > 0
        mock_loader.assert_called_once_with("dummy_path.pdf")
    
    def test_extract_text_from_documents(self):
        mock_docs = [
            Mock(page_content="First document content"),
            Mock(page_content="Second document content")
        ]
        
        result = self.processor.extract_text_from_documents(mock_docs)
        expected = "First document content\nSecond document content"
        
        assert result == expected
    
    @patch('src.utils.pdf_processor.PyPDFLoader')
    def test_validate_pdf_success(self, mock_loader):
        mock_doc = Mock()
        mock_doc.page_content = "Valid content"
        mock_loader.return_value.load.return_value = [mock_doc]
        
        result = self.processor.validate_pdf("valid.pdf")
        
        assert result is True
    
    @patch('src.utils.pdf_processor.PyPDFLoader')
    def test_validate_pdf_empty_content(self, mock_loader):
        mock_doc = Mock()
        mock_doc.page_content = "   "
        mock_loader.return_value.load.return_value = [mock_doc]
        
        result = self.processor.validate_pdf("empty.pdf")
        
        assert result is False
    
    @patch('src.utils.pdf_processor.PyPDFLoader')
    def test_validate_pdf_exception(self, mock_loader):
        mock_loader.side_effect = Exception("PDF loading failed")
        
        result = self.processor.validate_pdf("invalid.pdf")
        
        assert result is False
    
    @patch('src.utils.pdf_processor.PyPDFLoader')
    @patch('tempfile.NamedTemporaryFile')
    @patch('os.unlink')
    def test_process_uploaded_file(self, mock_unlink, mock_tempfile, mock_loader):
        mock_file = Mock()
        mock_file.name = "temp_file.pdf"
        mock_file.read.return_value = b"PDF content"
        
        mock_temp = Mock()
        mock_temp.name = "temp_file.pdf"
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=None)
        mock_tempfile.return_value = mock_temp
        
        mock_doc = Mock()
        mock_doc.page_content = "PDF content"
        mock_loader.return_value.load.return_value = [mock_doc]
        
        result = self.processor.process_uploaded_file(mock_file)
        
        assert len(result) > 0
        mock_unlink.assert_called_once()