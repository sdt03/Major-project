# import os
# from dotenv import load_dotenv
# import chromadb
# from sentence_transformers import SentenceTransformer
# from langchain.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_nvidia_ai_endpoints import ChatNVIDIA
# from stt import start_transcription
# from TTS import speak_text

# # Step 1: Load environment variables
# load_dotenv('/Users/shoumikdaterao/Desktop/Sem\\ 7/Project/code/code/.env.local')
# storage_path = os.getenv('STORAGE_PATH')
# if storage_path is None:
#     raise ValueError('STORAGE_PATH environment variable is not set')

# # Step 2: Set the NVIDIA API key
# nvapi_key = "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"
# assert nvapi_key.startswith("nvapi-"), f"{nvapi_key[:5]}... is not a valid key"
# os.environ["NVIDIA_API_KEY"] = nvapi_key

# # Step 3: Connect to ChromaDB
# client = chromadb.PersistentClient(path=storage_path)
# collection = client.get_collection(name="customer_support_chatbot_data")

# # Initialize NVIDIA model endpoint
# model_id = "meta/llama-3.1-70b-instruct"
# llm = ChatNVIDIA(model=model_id, temperature=0)

# # Step 4: Define the LangChain prompt template
# prompt = PromptTemplate(
#     template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an assistant for question-answering tasks.
#     Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
#     Use three sentences maximum and keep the answer concise <|eot_id|><|start_header_id|>user<|end_header_id|>
#     Question: {question}
#     Context: {context}
#     Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
#     input_variables=["question", "context"],
# )

# # Define the RAG chain using LangChain
# rag_chain = prompt | llm | StrOutputParser()

# # Function to format documents for context
# def format_docs(docs):
#     if docs and isinstance(docs[0], dict) and 'content' in docs[0]:
#         return "\n\n".join(doc['content'] for doc in docs)
#     else:
#         return "\n\n".join(str(doc) for doc in docs)

# # Step 5: Retrieve context from ChromaDB based on a query
# def retrieve_context_from_chromadb(query, num_results=3):
#     embedder = SentenceTransformer('all-MiniLM-L6-v2')
#     query_embedding = embedder.encode(query, convert_to_tensor=True).cpu()
    
#     results = collection.query(query_embeddings=[query_embedding.numpy()])
#     if 'documents' in results and results['documents']:
#         return results['documents'][:num_results]
#     else:
#         return []

# def generate_answer(question):
#     context_docs = retrieve_context_from_chromadb(question)
#     formatted_context = format_docs(context_docs)
    
#     try:
#         answer = rag_chain.invoke({"question": question, "context": formatted_context})
#         return answer or "No response generated."
#     except Exception as e:
#         print(f"Error in generating response: {e}")
#         return None

# # Main function
# if __name__ == "__main__":
#     # Step 6: Transcribe audio input as the question
#     #question = start_transcription()  # Transcribe audio to text from stt1.py
#     question = input("Ask your query: ")
    
#     # Generate an answer using the RAG pipeline
#     answer = generate_answer(question)
#     print("\nGenerated Answer:", answer)
#     speak_text(answer) # Speak the relevant answer generated
    
import os
from dotenv import load_dotenv
import chromadb
from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from stt import start_transcription

# Step 1: Load environment variables
load_dotenv('/Users/shoumikdaterao/Desktop/Sem\\ 7/Project/code/code/.env.local')
storage_path = os.getenv('STORAGE_PATH')
if storage_path is None:
    raise ValueError('STORAGE_PATH environment variable is not set')

# Step 2: Set the NVIDIA API key
nvapi_key = "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"
assert nvapi_key.startswith("nvapi-"), f"{nvapi_key[:5]}... is not a valid key"
os.environ["NVIDIA_API_KEY"] = nvapi_key

# Step 3: Connect to ChromaDB
client = chromadb.PersistentClient(path=storage_path)
collection = client.get_collection(name="customer_support_chatbot_data")

# Initialize NVIDIA model endpoint
model_id = "meta/llama-3.1-70b-instruct"
llm = ChatNVIDIA(model=model_id, temperature=0)

# Step 4: Define the LangChain prompt template
prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
    Use three sentences maximum and keep the answer concise <|eot_id|><|start_header_id|>user<|end_header_id|>
    Question: {question}
    Context: {context}
    Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "context"],
)

# Define the RAG chain using LangChain
rag_chain = prompt | llm | StrOutputParser()

# Function to format documents for context
def format_docs(docs):
    if docs and isinstance(docs[0], dict) and 'content' in docs[0]:
        return "\n\n".join(doc['content'] for doc in docs)
    else:
        return "\n\n".join(str(doc) for doc in docs)

# Step 5: Retrieve context from ChromaDB based on a query
def retrieve_context_from_chromadb(query, num_results=3):
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = embedder.encode(query, convert_to_tensor=True).cpu()
    
    results = collection.query(query_embeddings=[query_embedding.numpy()])
    if 'documents' in results and results['documents']:
        return results['documents'][:num_results]
    else:
        return []

def generate_answer(question):
    context_docs = retrieve_context_from_chromadb(question)
    formatted_context = format_docs(context_docs)
    
    try:
        answer = rag_chain.invoke({"question": question, "context": formatted_context})
        return answer or "No response generated."
    except Exception as e:
        print(f"Error in generating response: {e}")
        return "An error occurred while generating the response."

# Flask App
app = Flask(__name__)   
CORS(app, 
    resources={r"/*": {"origins": "*"}},
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"],
    supports_credentials=True,
)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Pong! Server is up and running."}), 200

@app.route("/")
def sayHello():
    return jsonify

@app.route("/ask", methods=["POST"])
def ask():
    try:
        app.logger.info("Received a request at /ask")
        data = request.get_json()
        app.logger.info(f"Request payload: {data}")
        
        question = data.get("question")
        if not question:
            app.logger.warning("No question provided in the request payload")
            return jsonify({"error": "No question provided"}), 400
        
        answer = generate_answer(question)
        app.logger.info(f"Generated answer: {answer}")
        return jsonify({"answer": answer}),200
    except Exception as e:
        app.logger.error(f"Error processing the question: {e}")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(port=5001)
    

