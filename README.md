# 🤖 llmini: Ollama Model System Profiler & Tester

Welcome to **llmini**! 🚀

A handy toolkit to **analyze your system hardware** and **suggest the best Ollama LLM models** for your machine, plus a script to **test your local Ollama server** and its models. Perfect for AI/ML enthusiasts, tinkerers, and anyone running LLMs locally! 🧑‍💻🖥️

---

## ✨ Features

- 🖥️ **System Profiler**: Detects your OS, RAM, CPU, GPU(s), disk type, and NPU.
- 🤔 **Model Suggestions**: Recommends the best Ollama models for your hardware.
- 🧪 **Ollama Model Tester**: Lists and tests all models running on your local Ollama server.
- 📝 **No third-party dependencies for core logic** (except for system info and HTTP requests).

---

## 📁 Project Structure

```
llmini/
├── suggest_ollama_models.py   # System profiler & model suggester 🖥️🤖
├── test_ollama_models.py      # Ollama model tester 🧪
├── requirements.txt           # Python dependencies 📦
├── dxdiag.txt                 # Example Windows system report 📝
└── README.md                  # This file! 📚
```

---

## 🖥️ suggest_ollama_models.py

- **Purpose:**
  - Detects your system specs (OS, RAM, CPU, GPU, disk, NPU).
  - Suggests the best Ollama models for your hardware.
- **How to use:**
  ```bash
  python suggest_ollama_models.py
  ```
- **Output:**
  - Prints your system info and recommended models with emoji hints!

---

## 🧪 test_ollama_models.py

- **Purpose:**
  - Connects to your local Ollama server (`http://localhost:11434`).
  - Lists all available models.
  - Sends a test prompt to each model and prints the response.
- **How to use:**
  1. Make sure [Ollama](https://ollama.com/) is running locally.
  2. Run:
     ```bash
     python test_ollama_models.py
     ```
- **Output:**
  - Lists models and shows a sample response for each.

---

## ⚙️ Installation & Setup

1. **Clone this repo:**
   ```bash
   git clone <your-repo-url>
   cd llmini
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   - _Tip: Use a virtual environment!_

---

## 📦 Requirements

- Python 3.7+
- [Ollama](https://ollama.com/) (for model testing)
- Python packages:
  - `psutil` (system info)
  - `requests` (HTTP requests)
  - `nvidia-ml-py3` (NVIDIA GPU info, optional)
  - `certifi`, `charset-normalizer`, `idna`, `urllib3` (HTTP stack)

---

## 🛠️ Example Usage

### 1. System Profiler & Model Suggester
```bash
python suggest_ollama_models.py
```
_Example output:_
```
Operating System: Windows (Version: Windows-11-10.0.26100-SP0)
Total RAM: 16.0 GB
CPU Cores: 12
GPU #1: NVIDIA GeForce GTX 1650 (Dedicated, VRAM: 4 GB)
  Type: Dedicated
  Volume: 4 GB
Storage: SSD 512 GB (Mounted at C:\)
NPU: Not detected

Suggested Ollama models for your system:
- ✅ llama2:7b, mistral, gemma:2b, codellama:7b [Best for 16GB RAM]
  🔽 ollama run llama2:7b
  🔽 ollama run mistral
  🔽 ollama run gemma:2b
  🔽 ollama run codellama:7b
💡 Dedicated GPU detected. Ollama with GPU acceleration recommended.
```

### 2. Ollama Model Tester
```bash
python test_ollama_models.py
```
_Example output:_
```
Available Ollama models:
- llama2:7b
- mistral
- gemma:2b

Model: llama2:7b
Response: Paris is the capital of France.
...
```

---

## 🙏 Acknowledgements

- [Ollama](https://ollama.com/) for their amazing local LLM platform.
- [psutil](https://github.com/giampaolo/psutil) for system info.
- [requests](https://docs.python-requests.org/) for HTTP requests.

---

## 🔗 Links

- Ollama Library: https://ollama.com/library
- Project Author: [Your Name Here]

---

> _Made with ❤️ and Python!_
