# 🚀 LinkedIn Post Generator

![Streamlit](https://img.shields.io/badge/Streamlit-Enabled-red)
![Groq](https://img.shields.io/badge/Groq-Accelerated-blue)
![LangChain](https://img.shields.io/badge/LangChain-Integrated-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A powerful and intuitive LinkedIn Post Generator powered by **Meta's LLaMA 3**, **LangChain**, **Streamlit**, and the lightning-fast **Groq API**. This tool helps content creators, job seekers, and professionals instantly craft engaging LinkedIn posts in multiple languages and formats with ease.

🔗 **Live Demo**: [Try it here](https://linkedin-post-generator-1.streamlit.app/)

---

## ✨ Features

- 🧠 Uses **LLaMA 3** via **Groq** for blazing-fast, high-quality text generation
- 🌍 Supports **multiple languages** including English, Hindi, Hinglish, and more
- 🏷️ Generate posts based on **custom tags** and **tone**
- 📝 Choose the **length** of your post (Short, Medium, Long)
- 🧩 Modular codebase using **LangChain** for prompt management and LLM orchestration
- 🎨 Clean and interactive **Streamlit UI**

---

## ⚙️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **LLaMA 3 (via Groq)** | LLM backend for post generation |
| **Streamlit** | Frontend UI for user interaction |
| **LangChain** | Prompt handling and LLM orchestration |
| **Python** | Core development language |
| **JSON/Pandas** | For storing and handling sample posts |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/linkedin-post-generator.git
cd linkedin-post-generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a .env file and add:
GROQ_API_KEY=your_groq_api_key

### 4. Run the app

```bash
streamlit run app.py
```

---
## 🧠 Future Improvements

- Add X (Twitter) post support
- Option to save/download generated posts
- User authentication for personal history
- Extend to image + text posts with Vision-LLaMA

---
