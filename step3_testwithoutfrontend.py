import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

print("1. Waking up the system...")
load_dotenv()

# Connect to Groq
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

# Connect to the local database we built in Step 2
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
database = Chroma(persist_directory="./my_local_db", embedding_function=embedding_model)

my_request = "the below is the customers email draft a response for it : your agreemnt is not compliant with the section 12 of the companies act"
print(f"\nYour Request: '{my_request}'")


print("\n2. Searching database for the best template...")

search_results = database.similarity_search(my_request, k=1)

# Extract the actual English text from the database result
found_template = search_results[0].page_content

# search_results = database.similarity_search(my_request, k=3)
# # We glue all 3 templates together with a divider so the AI can read them all
# found_templates = "\n\n--- NEXT TEMPLATE ---\n\n".join([doc.page_content for doc in search_results])
print("Found the template!")
print(f"\n{found_template}")


print("\n3. Sending instructions to the Brain...")


master_prompt = f"""
You are an expert email assistant. 
Draft an email reply to the USER REQUEST below. 
You can also refer to the information provided in the TEMPLATE.

TEMPLATE:
{found_template}

USER REQUEST:
{my_request}
"""

# Send it to Groq
response = llm.invoke(master_prompt)

# Print the final result!
print("\n================ FINAL EMAIL ================\n")
print(response.content)
print("\n=============================================")