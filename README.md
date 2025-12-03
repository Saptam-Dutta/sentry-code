# 🔒 SENTRY-CODE: AI-Powered Code Security Reviewer

An intelligent multi-agent AI system that automatically detects security vulnerabilities, provides LLM-generated explanations, and suggests automated patches.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-7%2F7%20Passing-brightgreen)

## 🎯 Features

- **Multi-Agent Architecture**: 6 specialized agents working in coordination
- **Smart Detection**: Rule-based SAST + heuristic analysis for 8+ vulnerability types
- **LLM Explanations**: AI-powered contextual security analysis using Ollama
- **Auto-Patching**: Generates and validates code fixes automatically
- **Interactive UI**: Beautiful Streamlit web application
- **Privacy-First**: Local LLM execution - your code never leaves your machine

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Ollama ([Download](https://ollama.ai/download))
- 8GB+ RAM recommended

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/sentry-code.git
cd sentry-code

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Pull LLM model
ollama pull llama3.2
```

### Running the Application
```bash
# Start Ollama (in separate terminal)
ollama serve

# Launch Streamlit UI
streamlit run ui/app.py
```

Visit `http://localhost:8501` in your browser.

## 📊 Performance Metrics

| Metric | Score | Target |
|--------|-------|--------|
| **Precision** | 78% | ≥75% ✅ |
| **Recall** | 85% | ≥60% ✅ |
| **F1-Score** | 81% | ≥67% ✅ |
| **Patch Success Rate** | 62% | - |

Tested on 50 code samples (30 vulnerable, 20 clean).

## 🏗️ Architecture
```
User Interface (Streamlit)
    ↓
Orchestrator Agent
    ↓
[Ingestor] → [Parser] → [SAST] → [LLM Reasoner] → [Patch Generator]
    ↓
Results Dashboard
```

### Agents

1. **Ingestor Agent**: File validation & metadata extraction
2. **Parser Agent**: AST generation for code structure analysis
3. **SAST Agent**: Rule-based vulnerability detection (8 rules)
4. **Heuristic Agent**: ML-based anomaly detection (future)
5. **LLM Reasoner**: AI-powered explanation generation (Ollama/Llama 3.2)
6. **Patch Generator**: Automated code fixing with validation

## 🔍 Supported Vulnerabilities

| Rule ID | Vulnerability | CWE | Severity |
|---------|---------------|-----|----------|
| PY001 | Hardcoded Credentials | CWE-798 | Critical |
| PY002 | SQL Injection | CWE-89 | Critical |
| PY003 | Code Injection (eval) | CWE-95 | Critical |
| PY004 | Disabled SSL Verification | CWE-295 | High |
| PY005 | Command Injection | CWE-78 | Critical |
| PY006 | Unsafe Deserialization | CWE-502 | Critical |
| PY007 | Weak Cryptography | CWE-327 | Medium |
| PY008 | Debug Mode Enabled | CWE-489 | Medium |

## 🧪 Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run evaluation
python scripts/run_evaluation.py
```

## 📁 Project Structure
```
sentry-code/
├── src/
│   ├── agents/          # All agent implementations
│   ├── rules/           # Vulnerability detection rules
│   ├── models/          # Data models (Pydantic)
│   └── utils/           # Helper functions
├── ui/                  # Streamlit application
├── tests/
│   └── fixtures/        # Test files (vulnerable & clean)
├── docs/                # Project documentation
└── scripts/             # Utility scripts
```

## 🛠️ Technology Stack

- **Language**: Python 3.12
- **LLM**: Ollama (Llama 3.2, Mistral, DeepSeek Coder)
- **UI**: Streamlit
- **Testing**: pytest
- **SAST**: Custom rules + AST parsing
- **Data Models**: Pydantic

## 📖 Documentation

- [Project Report](docs/PROJECT_REPORT_COMPLETE.md)
- [Architecture Details](docs/architecture.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🎓 Academic Context

**BCA 5th Semester - Generative AI Capstone Project**

This project demonstrates:
- Agentic AI system design
- LLM integration for code analysis
- Multi-agent orchestration
- Practical cybersecurity applications

**Author**: Saptam Kumar Dutta  
**Institution**: Chanakya University  
**Guide**: Anirudh Si

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OWASP for security guidelines and test cases
- Ollama team for local LLM infrastructure
- Streamlit for the amazing UI framework
- Project guide Anirudh Si for valuable feedback

## 📞 Contact

**Saptam Kumar Dutta**
- Email: saptam.dutta@example.com
- GitHub: [@saptamdutta](https://github.com/saptamdutta)
- LinkedIn: [Saptam Kumar Dutta](https://linkedin.com/in/saptamdutta)

---

⭐ If you find this project helpful, please consider giving it a star!

**Submission Date**: November 30, 2025  
**Course**: Generative AI - BCA 5th Semester  
**Academic Year**: 2024-25
