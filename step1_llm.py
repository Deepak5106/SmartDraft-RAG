import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

print("Waking up the AI...")

llm = ChatGroq(
    model="llama-3.1-8b-instant",  
    api_key=os.getenv("GROQ_API_KEY")
)

# 3. Send a test message to the AI
response = llm.invoke("Hi! If you can hear me, reply with exactly: 'Hello World, I am awake!'")

# 4. Print the AI's answer
print("\nAI Response:")
print(response.content)