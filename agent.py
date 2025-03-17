import os
import json
from typing import List
from datetime import datetime
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import Document
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import difflib

os.environ["GOOGLE_API_KEY"] = "AIzaSyD_4ojEIMUyMNgDoIjRtr7cPYzL7LVgS74"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def knowledge_base(file_path: str) -> List[Document]:
    if not os.path.exists(file_path):
        raise FileNotFoundError("Knowledge base file not found.")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Document(page_content=item["text"], metadata=item["metadata"]) for item in data]

def initialize_model():
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY is missing. Set it in your environment variables.")

    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=google_api_key, temperature=0.2)

def retrieve(question: str, documents: List[Document]) -> str:
    relevant_info = [doc.page_content for doc in documents if any(word in doc.page_content.lower() for word in question.lower().split())]
    return "\n".join(relevant_info) if relevant_info else "I could not find relevant information in my knowledge base."

def guardrails(response: str) -> str:
    restricted_terms = ["guaranteed returns", "sure profit", "insider trading"]
    for term in restricted_terms:
        if term in response.lower():
            return "I cannot provide financial guarantees or insider trading information. Please consult a licensed advisor."
    return response

def format_response(response: str) -> str:
    paragraphs = response.split('\n')
    unique_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if para and para not in unique_paragraphs:
            unique_paragraphs.append(para)
    
    formatted_response = "\n\n".join(unique_paragraphs)

    disclaimer = "\n\nDisclaimer: This is general financial information and not personalized investment advice."
    
    return f"{formatted_response}{disclaimer}"

def validate_numbers(response: str) -> str:
    if any(char.isdigit() for char in response):
        return f"{response}\n\nNote: Financial figures are approximations and may vary based on real-time data."
    return response

def chat():
    try:
        documents = knowledge_base("./knowledge_base/concepts.json")
        llm = initialize_model()
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        prompt_template = PromptTemplate(
            template=(
                "You are a trusted financial advisor, providing accurate and ethical financial guidance. "
                "Always base your answers strictly on the knowledge base provided and in short professional way. "
                "Do not make assumptions or provide speculative advice. "
                "If no relevant information is found, state that clearly."
                "\n\n"
                "Follow these formatting guidelines strictly:\n"
                "- Present information in clear, concise paragraphs\n"
                "- Use simple bullet points for lists when appropriate\n"
                "- Do not repeat information\n"
                "- Keep responses structured and easily readable\n"
                "- Do not use stars or symbols in your headings\n"
                "- Use plain text formatting\n"
                "\n"
                "Date: {current_date}\n\n"
                "User Query: {question}\n\n"
                "Relevant Knowledge:\n{context}\n\n"
                "Response:"
            ),
            input_variables=["current_date", "context", "question"]
        )

        print("\nFinancial Advisory is ready! Type your question below.")
        print("Type 'bye' to quit")
        print("-" * 30)

        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["bye"]:
                print("\nExiting... Goodbye!")
                break

            current_date = datetime.now().strftime("%Y-%m-%d")
            
            knowledge = retrieve(user_input, documents)
            ai_response = llm.invoke(prompt_template.format(
                current_date=current_date, 
                context=knowledge, 
                question=user_input
            ))
            
            validated_response = validate_numbers(ai_response.content)
            secure_response = guardrails(validated_response)
            final_response = format_response(secure_response)

            print("\nAdvisor:")
            print(f"{final_response}\n")
            print("-" * 30)

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    chat()