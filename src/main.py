import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
import tempfile
import os
import re
import random

# Streamlit UI
st.title("🤖 AI Interviewer & Candidate Shortlister")
st.write("Upload candidate resume and job description. The AI will conduct a 5-question interview, then evaluate and score the candidate.")

uploaded_resume = st.file_uploader("📄 Upload Candidate Resume (PDF)", type=["pdf"])
uploaded_client_doc = st.file_uploader("📑 Upload Job Description (PDF)", type=["pdf"])

if uploaded_resume and uploaded_client_doc:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_resume:
        tmp_resume.write(uploaded_resume.read())
        resume_path = tmp_resume.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_client:
        tmp_client.write(uploaded_client_doc.read())
        client_path = tmp_client.name

    # Load and process PDFs
    def load_and_split(path):
        loader = PyPDFLoader(path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        return text_splitter.split_documents(documents)

    resume_chunks = load_and_split(resume_path)
    client_chunks = load_and_split(client_path)

    # Local embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(client_chunks + resume_chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Use Ollama with Gemma model (no manual device setting)
    llm = Ollama(model="gemma3:4b")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
        verbose=False
    )

    st.subheader("🗣️ Interview Session")

    if "score" not in st.session_state:
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.total_questions = 5
        st.session_state.evaluations = []
        st.session_state.last_question = ""
        st.session_state.asked_questions = set()
        st.session_state.answer_submitted = False
        st.session_state.personality_indices = random.sample(range(5), 2)  # Ask 2 personality questions randomly

    def generate_unique_question():
        index = st.session_state.question_count
        if index in st.session_state.personality_indices:
            prompt = "Generate a short personality-based interview question that assesses traits like teamwork, resilience, leadership, or integrity. Do not explain the question."
        else:
            prompt = "Generate a short and clear technical or job-related interview question based on the job description and the candidate's resume. Do not provide any explanation or context."
            if st.session_state.evaluations:
                prompt += f" Take into account the previous answer: {st.session_state.evaluations[-1][1]} and make the next question a natural follow-up or explore a new but relevant topic."

        attempts = 0
        while attempts < 5:
            q = qa_chain.run(prompt).strip()
            if q not in st.session_state.asked_questions:
                st.session_state.asked_questions.add(q)
                return q
            attempts += 1
        return f"{q} (varied)"

    if st.session_state.question_count < st.session_state.total_questions:
        if not st.session_state.answer_submitted:
            if st.session_state.last_question == "":
                st.session_state.last_question = generate_unique_question()
            st.markdown(f"**Interviewer Bot (Q{st.session_state.question_count + 1}):** {st.session_state.last_question}")
            answer = st.text_input("👤 Your Answer:", key=f"answer_{st.session_state.question_count}")

            if st.button("Submit Answer"):
                if answer.strip():
                    eval_prompt = f"Evaluate this answer strictly on its relevance and quality for the job requirements and candidate traits. Respond with only a score from 1 to 10 and a short justification."
                    eval_prompt += f"\nAnswer: {answer}"
                    evaluation = qa_chain.run(eval_prompt)
                    score_match = re.search(r'(\b[1-9]\b|10)', evaluation)
                    score = int(score_match.group()) if score_match else 5

                    st.session_state.score += score
                    st.session_state.evaluations.append((st.session_state.last_question, answer, evaluation))
                    st.session_state.question_count += 1
                    st.session_state.last_question = ""
                    st.session_state.answer_submitted = False

    elif st.session_state.question_count == st.session_state.total_questions:
        st.subheader("📊 Final Evaluation")
        for i, (q, a, e) in enumerate(st.session_state.evaluations):
            st.markdown(f"**Q{i+1}:** {q}")
            st.markdown(f"**Candidate Answer:** {a}")
            st.markdown(f"**Evaluation:** {e}")
            st.markdown("---")

        final_score = st.session_state.score / st.session_state.total_questions
        st.markdown(f"### 🏁 Final Score: {final_score:.1f} / 10")

        if final_score >= 7:
            st.success("✅ Candidate is shortlisted.")
        else:
            st.error("❌ Candidate did not meet the criteria.")