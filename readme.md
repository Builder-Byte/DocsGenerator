# DocsGenerator 🚀

DocsGenerator is an automated **codebase documentation generator** that analyzes entire source-code repositories, extracts structural and semantic metadata, and produces **enterprise-grade documentation** using Large Language Models (LLMs).

It is designed for:
- Engineers onboarding into large codebases
- Teams maintaining legacy or fast-growing projects
- Automated documentation pipelines
- AI-assisted code understanding tools

DocsGenerator supports both **CLI-based workflows** and a **web-based interface** powered by FastAPI and a React frontend.

---

## 📌 Why DocsGenerator?

Modern codebases grow faster than documentation. DocsGenerator bridges this gap by:

- Automatically understanding code structure using AST parsing
- Mapping dependencies across files
- Generating clean, consistent, Markdown documentation
- Leveraging LLMs to explain intent, architecture, and usage

---

## ✨ Key Features

### 📂 Intelligent File Exploration
- Recursive directory traversal
- Configurable ignore rules (e.g. `node_modules`, `venv`, `.git`)
- Generates a project-wide file manifest with metadata

### 🧠 Static Code Analysis (AST-based)
- Extracts:
  - Imports (local and external)
  - Functions and parameters
  - Classes, inheritance, and methods
  - Type hints and return types
  - Constants and module-level variables
  - Docstrings
- Cross-file and cross-library dependency resolution

### 📝 Automated Documentation Generation
- Converts structured JSON analysis into Markdown
- Per-file documentation including:
  - Summary
  - Imports
  - Functions
  - Classes
  - Type hints
  - Constants
- Consistent and readable formatting

### 🤖 LLM-powered Code Summarization
- Produces human-friendly explanations for complex code
- Supports multiple LLM providers:
  - **Google Gemini**
  - **OpenRouter (Mistral)**
- Output quality suitable for:
  - Production documentation
  - Internal knowledge bases
  - New engineer onboarding

### 🌐 Web API + Frontend
- Upload a ZIP file containing a project
- Background processing with live status tracking
- Download final documentation as a ZIP archive
- Multi-user safe via session isolation

### 🧵 Multi-session & Scalable
- Each upload runs in an isolated session
- Independent output directories
- Safe for concurrent users

---

## 🏗️ Architecture Overview

```
Frontend (React + Vite)
        |
        v
FastAPI Backend
        |
        ├── ZIP Upload Handler
        ├── Session Manager
        ├── File Explorer
        ├── AST Dependency Generator
        ├── LLM Summarization Engine
        ├── Markdown Docs Generator
        └── ZIP Output Packager
```

---

## 🧩 Core Components

### Backend Modules

| Module | Description |
|------|------------|
| `server.py` | FastAPI server, session handling, background jobs, ZIP processing |
| `file_explorer_cli.py` | Reads files, filters directories, builds file manifests |
| `dependency_generator.py` | AST-based code analysis and dependency extraction |
| `docs_creator.py` | Converts JSON summaries into Markdown documentation |
| `gemini_client.py` | Google Gemini LLM client |
| `openrouter_client.py` | OpenRouter (Mistral) LLM client |
| `summarize.py` | Orchestrates full analysis + documentation pipeline |

### Frontend

- React
- Vite
- TypeScript
- Upload & status UI
- Download generated documentation

---

## 🛠️ Tech Stack

### Backend
- Python 3.9+
- FastAPI
- AST (Abstract Syntax Tree)
- Graphviz (optional, for AST visualization)

### Frontend
- React
- Vite
- TypeScript

### AI / LLM
- Google Gemini
- OpenRouter (Mistral)

---

## ⚙️ Configuration & Environment Variables

| Variable | Description |
|-------|------------|
| `GEMINI_API_KEY` | API key for Google Gemini |
| `OPENROUTER_API_KEY` | API key for OpenRouter |
| `BASE_DIR` | Root directory for uploads and outputs |

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Builder-Byte/DocsGenerator.git
cd DocsGenerator
```

---

### 2️⃣ Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

Set environment variables:

```bash
export GEMINI_API_KEY=your_key_here
export OPENROUTER_API_KEY=your_key_here
```

---

### 3️⃣ Frontend Setup

```bash
cd ../frontend
npm install
```

---

## ▶️ Usage

### 🔹 CLI Mode

1. Configure the target folder inside `summarize.py`
2. Run:

```bash
python summarize.py
```

📁 Output will be available in the `output/` directory.

---

### 🔹 Server Mode (Recommended)

#### Start Backend

```bash
fastapi dev backend/server.py
```

#### Start Frontend

```bash
cd frontend
npm run dev
```

Open your browser at:

```
http://localhost:5173
```

---

## 📂 Output Structure

```
output/
 └── session_id/
     └── project_name/
         ├── summary.md
         ├── file1.md
         ├── file2.md
         └── ...
```

---

## 🚧 Limitations & Notes

- Best results for Python, JavaScript, and TypeScript projects
- LLM output quality depends on model and API limits
- Extremely large repositories may take longer to process
- Graphviz is optional and only required for AST visualization

---

## 🛡️ Security Considerations

- Uploaded files are processed locally
- API keys should never be committed to source control
- CORS is fully open by default (restrict in production)

---

## 🧪 Future Improvements

- Language support beyond Python/JS/TS
- Incremental documentation updates
- GitHub integration
- Authentication and rate limiting
- Export formats beyond Markdown (PDF, HTML)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the **MIT License**.
