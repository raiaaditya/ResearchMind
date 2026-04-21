import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

# LLM setup
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=2048,
)

# --- AGENT PROMPTS ---

# 1. Search Agent: Generates a research query from user input
search_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a search query generator.\n"
     "Convert the user input into ONE short web search query.\n\n"
     "Rules:\n"
     "- Return ONLY the query\n"
     "- No explanation\n"
     "- No extra text\n"
     "- Max 10–12 words\n"
     "- Keep it simple and keyword-based\n"
     "- Include year (2024 or 2025) if relevant"
    ),
    ("human", "{input}")
])

# 2. Reader Agent: Extracts deep insights from Tavily results
reader_prompt = ChatPromptTemplate.from_messages([
    ("system", 
        "You are an expert research reader. Given a list of research snippets, extract:\n"
        "- Key arguments\n"
        "- Supporting evidence\n"
        "- Statistics\n"
        "- Conflicting viewpoints\n"
        "Return clean bullet points for each category. Be thorough and insightful."
    ),
    ("human", "{snippets}")
])

# 3. Writer Agent: Produces an analytical report
writer_prompt = ChatPromptTemplate.from_messages([
    ("system",
        "You are an analytical research writer. Using the extracted insights, write a structured report with:\n"
        "1. Introduction\n"
        "2. Analysis (compare sources, identify patterns/trends, highlight contradictions, generate insights)\n"
        "3. Key Insights (bullet points)\n"
        "4. Conclusion\n"
        "Be analytical, not just descriptive. Use evidence from the snippets."
    ),
    ("human", "{insights}")
])

# 4. Critic Agent: Evaluates the report and suggests improvements
critic_prompt = ChatPromptTemplate.from_messages([
    ("system",
        "You are a critical reviewer. Given a research report, provide:\n"
        "- Score out of 10\n"
        "- Strengths\n"
        "- Weaknesses\n"
        "- How to improve\n"
        "- One-line verdict\n"
        "Be concise and constructive."
    ),
    ("human", "{report}")
])

# --- AGENT FUNCTIONS ---

def search_agent(user_input):
    prompt = search_prompt.format(input=user_input)
    response = llm.invoke(prompt)
    return response.content.strip()

def reader_agent(snippets):
    prompt = reader_prompt.format(snippets=snippets)
    response = llm.invoke(prompt)
    return response.content.strip()

def writer_agent(insights):
    prompt = writer_prompt.format(insights=insights)
    response = llm.invoke(prompt)
    return response.content.strip()

def critic_agent(report):
    prompt = critic_prompt.format(report=report)
    response = llm.invoke(prompt)
    return response.content.strip()