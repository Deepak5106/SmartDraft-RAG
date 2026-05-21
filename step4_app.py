# python -m streamlit run step4_app.py
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
# sentence-transformers and torch are packages that get installed, but your code may not directly import them.
# Your code imports:
# from langchain_huggingface import HuggingFaceEmbeddings
# Internally, langchain_huggingface depends on:
# sentence-transformers
# torch
# hence install them in production ie the requirements.txt file


# In traditional frontend frameworks (like JavaScript/React), you are 100% correct. A button click triggers a specific event function, and the rest of the page stays still.
# But Streamlit does not work that way.
# In Streamlit, the entire script reruns from Line 1 to the very last line on every single button click. There is no way to stop this; it is how Streamlit is designed.
# Streamlit pauses the script for a microsecond.
# It looks at its hidden RAM dictionary and asks: "Have I ever run a function named load_brain_and_memory before?"
# If YES: It completely skips reading the code inside your function. It doesn't look at the disk. It doesn't check if files exist. It just reaches into its RAM, grabs the already-living llm and db objects, and attaches them right back to your script instantly.

st.set_page_config(page_title="AI Agent", page_icon="📧")
st.title("📧 Custom Email Agent")
st.write("Type your query, and the AI will write the perfect email based on your standard templates.")


# @st.cache_resource is a magic Streamlit command. 
# It keeps the AI loaded in the background so it doesn't have to 
# reboot the database every time you click "Generate".
@st.cache_resource
def load_brain_and_memory():
    load_dotenv()
    
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))
    
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if not os.path.exists("./my_local_db"):
        print("No database found! Building it now...")
        all_documents = []
        for filename in os.listdir("./data"):
            if filename.endswith(".txt"):
                loader = TextLoader(f"./data/{filename}", encoding="utf-8")
                all_documents.extend(loader.load())
        
        db = Chroma.from_documents(
            documents=all_documents, 
            embedding=embedding_model, 
            persist_directory="./my_local_db" 
        )
    else:
        db = Chroma(persist_directory="./my_local_db", embedding_function=embedding_model)
    return llm, db

llm, database = load_brain_and_memory()

user_request = st.text_area("What do you need an email for today?", height=150, placeholder="e.g., This setup is not compliant under the section 12 of companies act")

if st.button("Generate Email"):
    
    if user_request: 
        with st.spinner("Searching rulebook and writing email..."):
            
            search_results = database.similarity_search(user_request, k=1)
            found_template = search_results[0].page_content
            
            prompt = f"""
            You are a professional corporate email assistant.

            Your job is to generate a concise and professional email reply.

            RULES:
            - Use the retrieved reference ONLY as supporting context explain it if it seems relevant.
            - Do NOT add unnecessary explanations but also explain what the reference means.
            - Do NOT invent policies, offers, or additional assistance.
            - Keep the reply short but still explaining details from the reference unless the user explicitly asks for detail.
            - Stay semantically close to the retrieved reference.
            - If the template is relevant to the user's request, explain the template and how it applies to the user's request. If the template is not relevant, do not mention it at all.
            - Avoid overly polite filler sentences.

            MANDATORY EMAIL FORMAT:

            Start EXACTLY with:
            Dear Sir/Mam,

            Hope this email finds you well,

            End EXACTLY with:
            Best regards,

            REFERENCE:
            {found_template}

            USER REQUEST:
            {user_request}

            Generate the final email reply. 
            """
            
            response = llm.invoke(prompt)
            
            st.success("Email Generated!")
            st.write("---")
            st.write(response.content)
            
    else:
        st.warning("Please type a request into the box first!")