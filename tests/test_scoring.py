import pytest
from unittest.mock import Mock
from src.utils.scoring import InterviewScorer, EvaluationResult


class TestInterviewScorer:
    def setup_method(self):
        self.scorer = InterviewScorer(min_passing_score=7.0)
    
    def test_initialization(self):
        assert self.scorer.min_passing_score == 7.0
    
    def test_extract_score_from_evaluation_score_format(self):
        evaluation_text = "Score: 8 - Great technical knowledge"
        result = self.scorer.extract_score_from_evaluation(evaluation_text)
        assert result == 8
    
    def test_extract_score_from_evaluation_fraction_format(self):
        evaluation_text = "The candidate scored 7.5/10 on this question"
        result = self.scorer.extract_score_from_evaluation(evaluation_text)
        assert result == 8  # rounded
    
    def test_extract_score_from_evaluation_out_of_format(self):
        evaluation_text = "Rating: 6 out of 10"
        result = self.scorer.extract_score_from_evaluation(evaluation_text)
        assert result == 6
    
    def test_extract_score_from_evaluation_no_match(self):
        evaluation_text = "Good answer but no numeric score"
        result = self.scorer.extract_score_from_evaluation(evaluation_text)
        assert result == 5  # default
    
    def test_extract_score_boundary_values(self):
        # Test score clamping
        evaluation_text = "Score: 15"
        result = self.scorer.extract_score_from_evaluation(evaluation_text)
        assert result == 10  # clamped to max
        
        evaluation_text = "Score: -2"
        result = self.scorer.extract_score_from_evaluation(evaluation_text)
        assert result == 5  # default because -2 doesn't match pattern
    
    def test_evaluate_answer_empty_answer(self):
        result = self.scorer.evaluate_answer("What is Python?", "", None)
        
        assert isinstance(result, EvaluationResult)
        assert result.score == 1
        assert result.feedback == "No answer provided"
        assert result.question == "What is Python?"
        assert result.answer == ""
    
    def test_evaluate_answer_with_qa_chain(self):
        mock_qa_chain = Mock()
        mock_qa_chain.run.return_value = "Score: 8 - Excellent understanding of Python basics"
        
        result = self.scorer.evaluate_answer(
            "What is Python?", 
            "Python is a high-level programming language", 
            mock_qa_chain
        )
        
        assert result.score == 8
        assert "Excellent understanding" in result.feedback
        assert result.question == "What is Python?"
        assert result.answer == "Python is a high-level programming language"
    
    def test_evaluate_answer_qa_chain_exception(self):
        mock_qa_chain = Mock()
        mock_qa_chain.run.side_effect = Exception("API Error")
        
        result = self.scorer.evaluate_answer(
            "What is Python?", 
            "Python is a programming language", 
            mock_qa_chain
        )
        
        assert result.score == 5  # default on error
        assert "Evaluation error" in result.feedback
    
    def test_calculate_final_score_empty_evaluations(self):
        result = self.scorer.calculate_final_score([])
        
        expected = {
            'average_score': 0.0,
            'total_score': 0,
            'max_possible': 0,
            'percentage': 0.0,
            'passed': False
        }
        assert result == expected
    
    def test_calculate_final_score_with_evaluations(self):
        evaluations = [
            EvaluationResult(score=8, feedback="Good", question="Q1", answer="A1"),
            EvaluationResult(score=7, feedback="Okay", question="Q2", answer="A2"),
            EvaluationResult(score=9, feedback="Excellent", question="Q3", answer="A3")
        ]
        
        result = self.scorer.calculate_final_score(evaluations)
        
        assert result['average_score'] == 8.0
        assert result['total_score'] == 24
        assert result['max_possible'] == 30
        assert result['percentage'] == 80.0
        assert result['passed'] is True
    
    def test_get_performance_feedback_excellent(self):
        feedback = self.scorer.get_performance_feedback({'average_score': 9.5})
        assert "Excellent performance" in feedback
    
    def test_get_performance_feedback_very_good(self):
        feedback = self.scorer.get_performance_feedback({'average_score': 8.5})
        assert "Very good performance" in feedback
    
    def test_get_performance_feedback_good(self):
        feedback = self.scorer.get_performance_feedback({'average_score': 7.5})
        assert "Good performance" in feedback
    
    def test_get_performance_feedback_satisfactory(self):
        feedback = self.scorer.get_performance_feedback({'average_score': 6.5})
        assert "Satisfactory performance" in feedback
    
    def test_get_performance_feedback_below_average(self):
        feedback = self.scorer.get_performance_feedback({'average_score': 5.0})
        assert "Below average performance" in feedback
    
    def test_get_performance_feedback_poor(self):
        feedback = self.scorer.get_performance_feedback({'average_score': 3.0})
        assert "Poor performance" in feedback