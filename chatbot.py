from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage  # ✅ new import for v1.x

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file")

# Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

# Test the LLM
response = llm.invoke([HumanMessage(content="Give me one fun fact about space!")])

print("\n🤖 Gemini says:\n", response.content)
