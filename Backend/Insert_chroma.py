from datasets import load_dataset
import chromadb
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Load environment variables
load_dotenv('/Users/shoumikdaterao/Desktop/Sem\\ 7/Project/code/code/.env.local')
storage_path = os.getenv('STORAGE_PATH')
if storage_path is None:
    raise ValueError('STORAGE_PATH environment variable is not set')

# Initialize ChromaDB client
client = chromadb.PersistentClient(path=storage_path)
collection = client.get_or_create_collection(name="customer_support_chatbot_data")

# Load the dataset
dataset = load_dataset('bitext/Bitext-customer-support-llm-chatbot-training-dataset', split='train')

# Load models
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
ner = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

# Process and insert dataset
for idx, record in enumerate(dataset):
    # Combine instruction and response into a single string for embeddings
    content = f"Instruction: {record['instruction']}\nResponse: {record['response']}"

    # Extract metadata
    metadata = {
        'row': idx,  # Row ID
        'flags': record.get('flags'),
        'category': record.get('category'),
        'intent': record.get('intent'),
        'response': record.get('response'),
    }

    # Extract entities from instruction for enriched metadata
    entities = ner(record['instruction'])
    extracted_entities = {entity['entity_group']: entity['word'] for entity in entities}
    metadata.update(extracted_entities)  # Add extracted entities to metadata

    # Compute embeddings
    embedding = embedding_model.encode(content).tolist()  # Convert to list for serialization

    # Insert into ChromaDB
    collection.add(
        embeddings=[embedding],
        metadatas=[metadata],
        documents=[content],
        ids=[str(idx)]
    )

# Verify data insertion
total_documents = collection.count()
print(f"Total documents in collection: {total_documents}")

# Retrieve and print a sample for verification
retrieved_docs = collection.get()
print(f"Retrieved {len(retrieved_docs['documents'])} documents")
if retrieved_docs and 'documents' in retrieved_docs:
    for doc, meta in zip(retrieved_docs['documents'][:3], retrieved_docs['metadatas'][:3]):
        print(f"Document: {doc}")
        print(f"Metadata: {meta}")
