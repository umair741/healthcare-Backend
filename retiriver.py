from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file!")

PERSIST_DIR = "chroma_db"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve(query_text, top_k=3):
    query_embedding = model.encode([query_text]).tolist()[0]
    vectorstore = Chroma(collection_name="doctors", persist_directory=PERSIST_DIR)
    results = vectorstore.similarity_search_by_vector(query_embedding, k=top_k)
    return results

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    api_key=GOOGLE_API_KEY
)
prompt = ChatPromptTemplate.from_template("""
Hello! I am your virtual medical assistant from myguidance.io. 
I can help you find information about doctors, their specialties, clinics, experience, and other medical-related queries.

Follow these rules strictly:
1. If the user asks about specific doctors, clinics, specializations, or experience, use ONLY the context below to answer.
2. If the context does not contain the answer for a doctor-related query, reply politely:
   "I don't have this information in the documents."
3. For general medical questions (like "what should I do if I have a fever") or casual questions ("hi", "hello"), answer safely using your knowledge:
   - Do NOT give personal medical prescriptions or treatment.
   - Give general guidance and encourage consulting a qualified doctor.
4. Structure your answer clearly. For doctor information, include:
   - Name
   - Specialization
   - Clinic / Location
   - Experience
5. Be professional, concise, and friendly.

Context:
{context}

User Question:
{query}

Answer:
""")



def rag_chain(query):
    docs = retrieve(query)
    context = "\n".join([d.page_content for d in docs])
    final_prompt = prompt.format(context=context, query=query)
    response = llm.invoke(final_prompt)
    return response.content

if __name__ == "__main__":
    print("Doctor RAG System — Test Queries (type 'exit' to quit)")

    while True:
        user_query = input("\nEnter your query: ")

        if user_query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        try:
            answer = rag_chain(user_query)
            print("\n➡️ Answer:\n", answer)
        except Exception as e:
            print("⚠️ Error:", e)
