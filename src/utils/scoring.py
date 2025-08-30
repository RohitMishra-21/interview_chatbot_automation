import re
from typing import Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class EvaluationResult:
    score: int
    feedback: str
    question: str
    answer: str


class InterviewScorer:
    def __init__(self, min_passing_score: float = 7.0):
        self.min_passing_score = min_passing_score
        self.evaluation_prompt_template = """
        Evaluate this interview answer based on the following criteria:
        1. Relevance to the question (30%)
        2. Technical accuracy (25%)
        3. Communication clarity (25%)
        4. Depth of knowledge (20%)
        
        Provide a score from 1-10 and brief justification.
        
        Question: {question}
        Answer: {answer}
        
        Response format: Score: [1-10] - [Brief justification]
        """
    
    def extract_score_from_evaluation(self, evaluation_text: str) -> int:
        score_patterns = [
            r'Score:\s*(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*/\s*10',
            r'(\b[1-9]\b|10)',
            r'(\d+(?:\.\d+)?)\s*out\s*of\s*10'
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, evaluation_text, re.IGNORECASE)
            if match:
                score = float(match.group(1))
                return min(10, max(1, int(round(score))))
        
        return 5
    
    def evaluate_answer(self, question: str, answer: str, qa_chain) -> EvaluationResult:
        if not answer.strip():
            return EvaluationResult(
                score=1,
                feedback="No answer provided",
                question=question,
                answer=answer
            )
        
        evaluation_prompt = self.evaluation_prompt_template.format(
            question=question,
            answer=answer
        )
        
        try:
            evaluation_text = qa_chain.run(evaluation_prompt)
            score = self.extract_score_from_evaluation(evaluation_text)
            
            return EvaluationResult(
                score=score,
                feedback=evaluation_text,
                question=question,
                answer=answer
            )
        except Exception as e:
            return EvaluationResult(
                score=5,
                feedback=f"Evaluation error: {str(e)}",
                question=question,
                answer=answer
            )
    
    def calculate_final_score(self, evaluations: list) -> Dict[str, Any]:
        if not evaluations:
            return {
                'average_score': 0.0,
                'total_score': 0,
                'max_possible': 0,
                'percentage': 0.0,
                'passed': False
            }
        
        total_score = sum(eval_result.score for eval_result in evaluations)
        max_possible = len(evaluations) * 10
        average_score = total_score / len(evaluations)
        percentage = (total_score / max_possible) * 100
        
        return {
            'average_score': round(average_score, 1),
            'total_score': total_score,
            'max_possible': max_possible,
            'percentage': round(percentage, 1),
            'passed': average_score >= self.min_passing_score
        }
    
    def get_performance_feedback(self, final_results: Dict[str, Any]) -> str:
        score = final_results['average_score']
        
        if score >= 9:
            return "Excellent performance! Outstanding knowledge and communication skills."
        elif score >= 8:
            return "Very good performance. Strong candidate with solid expertise."
        elif score >= 7:
            return "Good performance. Meets the requirements with room for growth."
        elif score >= 6:
            return "Satisfactory performance. Some areas need improvement."
        elif score >= 4:
            return "Below average performance. Significant gaps identified."
        else:
            return "Poor performance. Major improvements needed."