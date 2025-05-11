# GenieRAG
GenieRAG: Intelligent Question-Answering with Retrieval-Augmented Generation (RAG) A smart AI agent that combines retrieval-based search and generative language models to deliver accurate answers from your custom knowledge base.

---

# 🛠️ Project Setup

🔁 Clone the Repository

```bash
git clone https://github.com/pintuprajapati/GenieRAG.git
```

---

### 💡 Environment Setup

🔹 Create and Activate Virtual Environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🔐 Environment Variables

1. Copy the .env.sample file and rename it to .env:

```bash
cp .env.sample .env
```

2. Fill in the necessary values inside .env as needed (e.g., API keys, etc.).

---

### Note: You'll need to open two terminals to run the project (server + UI)

# 🚀 Run the FastAPI Server

Open Terminal one

```bash
python main.py
```

Your FastAPI app should now be running on:

```
http://127.0.0.1:8000
```


---

### 📬 API Docs

FastAPI automatically provides interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

# 🚀 Run the Streamlit Server
Open Terminal Two
```bash
streamlit run app.py
```

Your FastAPI app should now be running on:

```
http://localhost:8501
```

---

✨ Author

Pintu Rajpati  
Feel free to connect or contribute!

---

