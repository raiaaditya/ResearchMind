# Quick Start Guide

## 🚀 Fast Setup (2 minutes)

### 1. Set Environment Variables

**Windows (PowerShell)**:
```powershell
$env:GROQ_API_KEY = "your_groq_key_here"
$env:TAVILY_API_KEY = "your_tavily_key_here"
```

**Or create `.env` file**:
```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Pipeline
```bash
# Windows (UTF-8 for emojis)
$env:PYTHONIOENCODING='utf-8'; python pipeline.py

# macOS/Linux
python pipeline.py
```

---

## 📊 Pipeline Output Structure

```
Step 1: Search Agent generates query
  ↓
Step 2: Tavily finds 5 URLs
  ↓
Step 3: Reader extracts insights from 3 URLs
  ↓
Step 4: Writer compiles structured report
  ↓
Step 5: Critic evaluates report (Score/10)
```

---

## 🎯 Example Output

```
🔍 STEP 1 - SEARCH AGENT
Generated Search Query: "latest artificial intelligence developments 2024"

🌐 STEP 2 - TAVILY WEB SEARCH
✅ Found 5 results:
1. Algotive - AI Trends
2. TheCodeWork - Top 10 Developments
3. NewMetrics - AI Trends 2024
[...]

📖 STEP 3 - READER AGENT
✅ Extracted insights from 3 URLs

📝 SCRAPED INSIGHTS
- Machine learning improvements
- 55% companies invested in AI
- Ethical guidelines needed
[...]

✍️ STEP 4 - WRITER AGENT
📄 FINAL RESEARCH REPORT
**Introduction**
[Full structured report...]

🔎 STEP 5 - CRITIC AGENT
💬 CRITIC FEEDBACK
Score: 6/10
Strengths: ...
Weaknesses: ...
```

---

## 🔧 File Reference

| File | Purpose | Key Functions |
|------|---------|---|
| `agents.py` | Define 4 agents | `build_search_agent`, `build_reader_agent`, `writer_chain`, `critic_chain` |
| `pipeline.py` | Orchestration | `run_research_pipeline()`, `search_web()`, `scrape_url()` |
| `tools.py` | Utilities | `web_search()`, `scrape_url()` tools |
| `requirements.txt` | Dependencies | All Python packages needed |

---

## 🐛 Troubleshooting

### Error: "Invalid API Key"
- ✅ Check `.env` file exists
- ✅ Verify `GROQ_API_KEY` and `TAVILY_API_KEY` are set
- ✅ Keys shouldn't have quotes in `.env`

### Error: "Query is too long"
- ✅ Fixed! Search query now limited to 400 chars

### Error: "UnicodeEncodeError"
- ✅ Use: `$env:PYTHONIOENCODING='utf-8'; python pipeline.py`

### Error: "Import Error"
- ✅ Run: `pip install -r requirements.txt`

---

## 💡 Customization

### Change Research Topic
Edit line 197 in `pipeline.py`:
```python
topic = "Your custom topic here"
```

### Adjust Number of URLs
Change line 77 in `pipeline.py`:
```python
for i, result in enumerate(search_results[:5], 1):  # Changed from :3 to :5
```

### Change LLM Model
Edit line 16 in `agents.py`:
```python
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # Change this
)
```

---

## 📈 Architecture Overview

```
┌─────────────────────────────────────┐
│   RESEARCH TOPIC INPUT              │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   SEARCH AGENT (ChatGroq + Prompt)  │
│   Output: Concise search query      │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   TAVILY WEB SEARCH                 │
│   Output: 5 URLs with content       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   READER AGENT (Process 3 URLs)     │
│   Output: Bullet-point insights     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   WRITER AGENT                      │
│   Output: Structured report         │
│   - Introduction                    │
│   - Key Findings                    │
│   - Conclusion                      │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   CRITIC AGENT                      │
│   Output: Evaluation                │
│   - Score /10                       │
│   - Strengths                       │
│   - Weaknesses                      │
│   - Verdict                         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   FINAL OUTPUT & STATE DICT         │
└─────────────────────────────────────┘
```

---

## 🎓 What Each Agent Does

### 🔍 Search Agent
- **Input**: Research topic
- **LLM**: ChatGroq (llama-3.3-70b-versatile)
- **Output**: Concise web search query (max 400 chars)
- **Purpose**: Converts natural language topic to searchable query

### 🌐 Web Search
- **Input**: Search query
- **Tool**: Tavily API
- **Output**: List of 5 URLs with titles & snippets
- **Purpose**: Find relevant sources

### 📖 Reader Agent
- **Input**: URL content (scraped HTML)
- **LLM**: ChatGroq
- **Output**: Bullet-point insights
- **Purpose**: Extract key information from pages

### ✍️ Writer Agent
- **Input**: Topic + Combined research insights
- **LLM**: ChatGroq
- **Output**: Structured report
- **Purpose**: Compile findings into coherent narrative

### 🔎 Critic Agent
- **Input**: Generated report
- **LLM**: ChatGroq
- **Output**: Evaluation with score & feedback
- **Purpose**: Quality assessment & improvement suggestions

---

## 🔑 API Keys

### Get Groq Key
1. Visit: https://console.groq.com/
2. Sign up (free)
3. Create API key
4. Copy to `.env`

### Get Tavily Key
1. Visit: https://tavily.com/
2. Sign up (free tier available)
3. Get API key
4. Copy to `.env`

---

## ✅ Verification Checklist

- [ ] Python 3.10+ installed
- [ ] `.env` file created with API keys
- [ ] `pip install -r requirements.txt` completed
- [ ] All imports work: `python -c "from agents import *"`
- [ ] Run: `python pipeline.py` successfully
- [ ] See all 5 steps completed in output

---

**Status**: ✅ Ready to use!
