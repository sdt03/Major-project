# import pandas as pd
# from transformers import AutoTokenizer, AutoModelForCausalLM
# from bert_score import score
# import chromadb
# import os
# from dotenv import load_dotenv
# from sentence_transformers import SentenceTransformer

# # Step 1: Load environment variables
# load_dotenv('/Users/shoumikdaterao/Desktop/Sem\\ 7/Project/code/code/.env.local')
# storage_path = os.getenv('STORAGE_PATH')
# if storage_path is None:
#     raise ValueError('STORAGE_PATH environment variable is not set')

# # Initialize ChromaDB client and collection
# client = chromadb.PersistentClient(path=storage_path)
# collection = client.get_collection(name="customer_support_chatbot_data")

# # Load the tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained("khalednabawi11/fine_tuned_dialo-gpt")
# model = AutoModelForCausalLM.from_pretrained("khalednabawi11/fine_tuned_dialo-gpt")

# # Sentence Transformer for query embeddings
# embedder = SentenceTransformer('all-MiniLM-L6-v2')

# # Retrieve relevant context from ChromaDB
# def retrieve_context(question, num_results=3):
#     try:
#         # Encode the question to get its embedding
#         query_embedding = embedder.encode(question, convert_to_tensor=True).cpu().numpy()

#         # Query the ChromaDB collection to retrieve the most relevant documents
#         results = collection.query(query_embeddings=[query_embedding], n_results=num_results)

#         # Extract documents from the query results
#         documents = results.get("documents", [[]])[0]
#         if documents:
#             # Return the context by joining the retrieved documents
#             return "\n\n".join(doc for doc in documents)
#         else:
#             return "No relevant context found."
#     except Exception as e:
#         return f"Error retrieving context: {e}"

# # Function to generate responses using RAG
# def generate_response(question):
#     # Retrieve the context for the question
#     context = retrieve_context(question)
    
#     # Log the retrieved context for debugging
#     print(f"Retrieved context for question '{question}':\n{context}")
    
#     # Handle case when no relevant context is found
#     if context.strip() == "No relevant context found.":
#         return "I couldn't find any relevant context to answer this question."
    
#     # Prepare the input text for the model
#     input_text = f"Context: {context}\n\nQuestion: {question}"
    
#     # Encode the input text using the tokenizer
#     inputs = tokenizer(input_text + tokenizer.eos_token, return_tensors="pt")
    
#     # Generate the response
#     outputs = model.generate(
#         inputs["input_ids"],
#         max_new_tokens=1,
#         pad_token_id=tokenizer.eos_token_id,
#         num_return_sequences=1,
#         temperature=0.9,  # Increased temperature for diversity
#         top_p=0.95       # Use nucleus sampling for more varied responses
#     )
    
#     # Decode and return the model's response
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     print(f"Generated response: {response}")
#     return response

# csv_file_path = r"/Users/shoumikdaterao/Desktop/Sem 7/Project/code/Customer Support/Backend/STF/rag_evaluation_results_CANCEL.csv"
# data = pd.read_csv(csv_file_path)

# # Generate responses for all questions
# data["model_response"] = data["Question"].apply(lambda q: generate_response(q) if pd.notna(q) else "No question provided.")

# # Prepare references and predictions for evaluation
# references = data["Expected_Answer"].fillna("").tolist()
# predictions = data["model_response"].fillna("").tolist()

# # Compute BERTScore to evaluate the model's performance
# try:
#     P, R, F1 = score(predictions, references, lang="en")

#     # Add BERTScore metrics to the DataFrame
#     data["Precision"] = P.tolist()
#     data["Recall"] = R.tolist()
#     data["F1"] = F1.tolist()

#     # Display average scores
#     print(f"Average Precision: {P.mean():.4f}")
#     print(f"Average Recall: {R.mean():.4f}")
#     print(f"Average F1 Score: {F1.mean():.4f}")
# except Exception as e:
#     print(f"Error computing BERTScore: {e}")

# # Save the results to a CSV file
# output_file_path = r"/Users/shoumikdaterao/Desktop/Sem 7/Project/code/Customer Support/Backend/STF/rag_evaluation_results_CANCEL_part2.csv"
# data.to_csv(output_file_path, index=False)
# print(f"Results saved to {output_file_path}")

import pandas as pd
from bert_score import score
from rag import generate_answer

# Path to the CSV file containing test cases
csv_file_path = r"/Users/shoumikdaterao/Desktop/Sem 7/Project/code/Customer Support/Filtered test cases/shipping_subscription.xlsx"

# Load the test cases
test_cases = pd.read_excel(csv_file_path)

# Ensure the required columns exist
required_columns = ["category", "question", "expected_answers"]
if not all(column in test_cases.columns for column in required_columns):
    raise ValueError(f"The CSV file must contain the following columns: {required_columns}")

# Store model responses
model_responses = []
precision_scores = []
recall_scores = []
f1_scores = []

# Evaluate responses
def evaluate_responses(test_cases):
    global model_responses, precision_scores, recall_scores, f1_scores
    questions = test_cases["question"].tolist()
    references = test_cases["expected_answers"].tolist()

    # Generate responses for each question
    for question in questions:
        response = generate_answer(question)
        model_responses.append(response)

    # Evaluate using BERTScore
    P, R, F1 = score(model_responses, references, lang="en")

    # Store precision, recall, and F1 scores for each response
    precision_scores.extend(P.tolist())
    recall_scores.extend(R.tolist())
    f1_scores.extend(F1.tolist())

    evaluation_results = {
        "precision": P.mean().item(),
        "recall": R.mean().item(),
        "f1": F1.mean().item()
    }
    return evaluation_results

# Run evaluation and save results
if __name__ == "__main__":
    print("Evaluating responses...")
    results = evaluate_responses(test_cases)

    # Add responses and scores to the DataFrame
    test_cases["Model_Response"] = model_responses
    test_cases["Precision"] = precision_scores
    test_cases["Recall"] = recall_scores
    test_cases["F1_Score"] = f1_scores

    # Save the results to a CSV file
    output_csv_path = r"/Users/shoumikdaterao/Desktop/Sem 7/Project/code/Customer Support/Results/LLAMA_RESULTS/Filtered_shipping_subscription_EVAL_llama.csv"
    test_cases.to_csv(output_csv_path, index=False)
    print(f"Evaluation complete. Results saved to {output_csv_path}")
    print(f"Average Precision: {results['precision']:.4f}")
    print(f"Average Recall: {results['recall']:.4f}")
    print(f"Average F1 Score: {results['f1']:.4f}")
