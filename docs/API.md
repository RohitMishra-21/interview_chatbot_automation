# API Documentation

## Overview

The AI Interview Assistant is built with a modular architecture that separates concerns into distinct components. This document outlines the main classes and their methods.

## Core Components

### PDFProcessor (`src/utils/pdf_processor.py`)

Handles PDF document processing and text extraction.

#### Methods

```python
class PDFProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100)
    
    def process_uploaded_file(self, uploaded_file) -> List[Document]
    """Process an uploaded file and return document chunks."""
    
    def load_and_split(self, file_path: str) -> List[Document]
    """Load PDF from file path and split into chunks."""
    
    def extract_text_from_documents(self, documents: List[Document]) -> str
    """Extract plain text from document chunks."""
    
    def validate_pdf(self, file_path: str) -> bool
    """Validate if PDF file is readable and contains content."""
```

### InterviewScorer (`src/utils/scoring.py`)

Handles evaluation and scoring of interview responses.

#### Methods

```python
class InterviewScorer:
    def __init__(self, min_passing_score: float = 7.0)
    
    def extract_score_from_evaluation(self, evaluation_text: str) -> int
    """Extract numeric score from evaluation text."""
    
    def evaluate_answer(self, question: str, answer: str, qa_chain) -> EvaluationResult
    """Evaluate a candidate's answer and return detailed results."""
    
    def calculate_final_score(self, evaluations: list) -> Dict[str, Any]
    """Calculate final interview scores and statistics."""
    
    def get_performance_feedback(self, final_results: Dict[str, Any]) -> str
    """Generate human-readable performance feedback."""
```

### InterviewUI (`src/components/interview_ui.py`)

Manages the Streamlit user interface components.

#### Methods

```python
class InterviewUI:
    def render_header()
    """Render the application header and title."""
    
    def render_file_upload_section() -> Tuple[Optional[any], Optional[any]]
    """Render file upload widgets for resume and job description."""
    
    def render_interview_progress(current_question: int, total_questions: int)
    """Display interview progress bar."""
    
    def render_question_section(question: str, question_number: int) -> str
    """Render interview question and answer input."""
    
    def render_evaluation_section(evaluations: list)
    """Display evaluation results for all questions."""
    
    def render_final_results(final_results: dict, performance_feedback: str)
    """Display final scoring and recommendation."""
```

## Data Models

### EvaluationResult

```python
@dataclass
class EvaluationResult:
    score: int
    feedback: str
    question: str
    answer: str
```

### InterviewSession

```python
@dataclass
class InterviewSession:
    session_id: str
    candidate_name: Optional[str]
    position: Optional[str]
    questions: List[InterviewQuestion]
    answers: List[CandidateAnswer]
    evaluations: List[QuestionEvaluation]
    started_at: datetime
    completed_at: Optional[datetime]
    status: str
```

## Configuration

### Environment Variables

- `OLLAMA_HOST`: Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL`: LLM model name (default: gemma3:4b)
- `MAX_QUESTIONS`: Number of interview questions (default: 5)
- `MIN_PASSING_SCORE`: Minimum score to pass (default: 7.0)
- `EMBEDDING_MODEL`: Sentence transformer model (default: all-MiniLM-L6-v2)

## Usage Examples

### Basic Usage

```python
from src.utils.pdf_processor import PDFProcessor
from src.utils.scoring import InterviewScorer

# Initialize components
pdf_processor = PDFProcessor()
scorer = InterviewScorer(min_passing_score=7.0)

# Process documents
resume_docs = pdf_processor.process_uploaded_file(uploaded_resume)
job_docs = pdf_processor.process_uploaded_file(uploaded_job_desc)

# Evaluate answers
evaluation = scorer.evaluate_answer(question, answer, qa_chain)
final_results = scorer.calculate_final_score([evaluation])
```

### Error Handling

All components include proper error handling:

```python
try:
    documents = pdf_processor.process_uploaded_file(file)
except Exception as e:
    logger.error(f"PDF processing failed: {e}")
    # Handle error appropriately
```

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

## Extending the System

### Adding New Question Types

1. Extend the `QuestionType` enum in `src/models/interview_models.py`
2. Update question generation logic in the main application
3. Add appropriate test cases

### Custom Scoring Algorithms

1. Subclass `InterviewScorer`
2. Override the `evaluate_answer` method
3. Implement custom scoring logic

### UI Customization

1. Extend `InterviewUI` class
2. Add new rendering methods
3. Update the main application to use new components