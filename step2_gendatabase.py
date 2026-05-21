import os
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

print("1. Scanning your data folder for templates...")

# UPGRADE: A simple loop that finds every .txt file in the folder and reads it
all_documents = []
for filename in os.listdir("./data"):
    if filename.endswith(".txt"):
        print(f" -> Found: {filename}")
        loader = TextLoader(f"./data/{filename}")
        all_documents.extend(loader.load())

print(f"\nTotal templates loaded: {len(all_documents)}")
print("2. Firing up the Math Translator...")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("3. Building the new database...")
database = Chroma.from_documents(
    documents=all_documents, 
    embedding=embedding_model, 
    persist_directory="./my_local_db" 
)

print("\nSuccess! All templates are now permanently saved in your local memory.")