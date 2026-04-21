# 🧠 ResearchMind – Multi-Agent AI Research System

ResearchMind is a multi-agent AI system that automates the complete research pipeline — from generating search queries to producing structured analytical reports with evaluation. It mimics how a human researcher works using multiple AI agents collaborating step-by-step.

---

## 🚀 Features

- 🔍 Search Agent – Generates optimized search queries  
- 🌐 Tavily Fetch – Retrieves real-time web data  
- 📖 Reader Agent – Extracts key insights, arguments, and evidence  
- ✍️ Writer Agent – Produces structured analytical reports  
- 🔎 Critic Agent – Evaluates report quality with score and feedback  

---

## 🧩 Workflow

User Input → Search Agent → Tavily Fetch → Reader Agent → Writer Agent → Critic Agent  

---

## 💻 Tech Stack

- Python  
- LangChain  
- Groq API  
- Tavily API  
- Streamlit  
- BeautifulSoup  

---

## 📊 Highlights

- ⚡ Real-time pipeline visualization  
- ⏳ Step-by-step execution tracking  
- 🎨 Clean dark-themed UI  
- 📈 Metrics (sources, word count, score)  
- 📄 Downloadable final report  

---

## 🛠️ Setup

1. Clone the repository  
2. Navigate into the project folder  
3. Create a virtual environment  
4. Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file and add:

```
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
```

⚠️ Do NOT upload this file to GitHub  

---

## ▶️ Run

### CLI Version
```bash
python pipeline.py
```

### Streamlit UI
```bash
streamlit run app.py
```

---

## 📌 Use Cases

- Academic research automation  
- Market analysis  
- Technology trend exploration  
- Policy & geopolitical research  

---

## 📈 Output

- Structured research reports  
- Key insights & arguments  
- Conflicting viewpoints  
- Critic evaluation with score  

---

## 🔮 Future Improvements

- RAG (Retrieval-Augmented Generation)  
- Vector database integration  
- Multi-query research  
- PDF export  
- Citation generation  

---

## 👨‍💻 Author

Aaditya Rai  

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
