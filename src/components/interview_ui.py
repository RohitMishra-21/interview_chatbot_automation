import streamlit as st
from typing import Optional, Tuple


class InterviewUI:
    def __init__(self):
        self.setup_page_config()
    
    def setup_page_config(self):
        st.set_page_config(
            page_title="AI Interview Assistant",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_header(self):
        st.title("🤖 AI Interview Assistant")
        st.markdown("""
        Upload candidate resume and job description. The AI will conduct a structured interview 
        and provide detailed evaluation and scoring.
        """)
        st.divider()
    
    def render_file_upload_section(self) -> Tuple[Optional[any], Optional[any]]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Candidate Resume")
            uploaded_resume = st.file_uploader(
                "Upload Resume (PDF)", 
                type=["pdf"],
                key="resume_upload",
                help="Upload the candidate's resume in PDF format"
            )
        
        with col2:
            st.subheader("📑 Job Description")
            uploaded_job_desc = st.file_uploader(
                "Upload Job Description (PDF)", 
                type=["pdf"],
                key="job_desc_upload",
                help="Upload the job requirements and description in PDF format"
            )
        
        return uploaded_resume, uploaded_job_desc
    
    def render_interview_progress(self, current_question: int, total_questions: int):
        progress_percentage = current_question / total_questions
        st.progress(progress_percentage)
        st.caption(f"Question {current_question} of {total_questions}")
    
    def render_question_section(self, question: str, question_number: int) -> str:
        st.subheader(f"🗣️ Interview Question #{question_number}")
        st.markdown(f"**Interviewer:** {question}")
        
        answer = st.text_area(
            "👤 Your Response:",
            key=f"answer_{question_number}",
            height=150,
            placeholder="Type your answer here..."
        )
        
        return answer
    
    def render_evaluation_section(self, evaluations: list):
        st.subheader("📊 Interview Evaluation")
        
        for i, eval_result in enumerate(evaluations, 1):
            with st.expander(f"Question {i} - Score: {eval_result.score}/10"):
                st.markdown(f"**Q:** {eval_result.question}")
                st.markdown(f"**A:** {eval_result.answer}")
                st.markdown(f"**Evaluation:** {eval_result.feedback}")
    
    def render_final_results(self, final_results: dict, performance_feedback: str):
        st.subheader("🏁 Final Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Average Score",
                f"{final_results['average_score']}/10",
                delta=None
            )
        
        with col2:
            st.metric(
                "Total Score",
                f"{final_results['total_score']}/{final_results['max_possible']}",
                delta=None
            )
        
        with col3:
            st.metric(
                "Percentage",
                f"{final_results['percentage']}%",
                delta=None
            )
        
        if final_results['passed']:
            st.success(f"✅ **PASSED** - {performance_feedback}")
        else:
            st.error(f"❌ **NOT QUALIFIED** - {performance_feedback}")
    
    def render_sidebar_info(self):
        with st.sidebar:
            st.header("ℹ️ How it works")
            st.markdown("""
            1. **Upload Documents**: Resume and job description (PDF)
            2. **AI Processing**: Documents are analyzed using advanced NLP
            3. **Dynamic Interview**: AI generates relevant questions
            4. **Real-time Scoring**: Each answer is evaluated immediately
            5. **Final Assessment**: Comprehensive evaluation and recommendation
            """)
            
            st.header("🛠️ Features")
            st.markdown("""
            - **Smart Question Generation**
            - **Technical & Behavioral Questions**
            - **Detailed Scoring System**
            - **Performance Analytics**
            - **Local AI Processing**
            """)
    
    def show_loading(self, message: str = "Processing..."):
        return st.spinner(message)
    
    def show_error(self, message: str):
        st.error(f"❌ {message}")
    
    def show_success(self, message: str):
        st.success(f"✅ {message}")
    
    def show_warning(self, message: str):
        st.warning(f"⚠️ {message}")