# 🤖 AI Interview Assistant

An intelligent interviewing system that conducts automated interviews and evaluates candidates based on their resumes and job requirements using advanced AI technology.

## 🚀 Features

- **Smart PDF Processing**: Upload candidate resumes and job descriptions in PDF format
- **AI-Powered Interviews**: Conducts structured 5-question interviews with dynamic question generation
- **Intelligent Scoring**: Evaluates candidate responses with detailed feedback
- **Vector-Based Retrieval**: Implements FAISS for efficient document similarity search
- **Interactive UI**: Built with Streamlit for seamless user experience

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Gemma model downloaded via HuggingFace

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/ai-interview-assistant.git
cd ai-interview-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Download the Gemma model:
```bash
huggingface-cli download <repo_id>
```

## 🎯 Usage

1. Start the application:
```bash
streamlit run src/main.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload candidate resume and job description (PDF format)

4. Conduct the AI-powered interview session

5. Review evaluation results and scoring

## 📁 Project Structure

```
ai-interview-assistant/
├── src/
│   ├── main.py              # Main Streamlit application
│   ├── components/          # UI components
│   ├── utils/              # Utility functions
│   └── models/             # Data models
├── tests/                  # Test files
├── docs/                   # Documentation
├── examples/               # Example files
├── scripts/                # Utility scripts
├── data/                   # Sample data
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🧪 Testing

Run tests using:
```bash
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the web interface
- [LangChain](https://langchain.com/) for LLM orchestration
- [FAISS](https://faiss.ai/) for vector similarity search

## 📞 Support

For support, email support@example.com or open an issue on GitHub.
