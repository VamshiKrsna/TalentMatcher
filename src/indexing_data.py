import faiss
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = 'job_candidates'
COLLECTION_NAME = 'candidates'

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Load the SentenceTransformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Fetch documents from MongoDB and extract 'description' fields
documents = list(collection.find({}, {'_id': 0}))
# print(documents)

data = []
for doc in documents:
    person_info = {
        'Name': doc.get('Name', 'N/A'),
        'Contact Details': doc.get('Contact Details', 'N/A'),
        'Location': doc.get('Location', 'N/A'),
        'Job Skills': doc.get('Job Skills', 'N/A'),
        'Experience': doc.get('Experience', 'N/A'),
        'Projects': doc.get('Projects', 'N/A'),
        'Comments': doc.get('Comments', 'N/A')
    }
    data.append(person_info)

# for person in data:
#     print(person)

# Generate embeddings for the documents
embeddings = model.encode(data)
embeddings = np.array(embeddings, dtype='float32')

# Create a FAISS index
dimension = embeddings.shape[1]  # Dimension of the vectors
index = faiss.IndexFlatL2(dimension)  # L2 distance index
index.add(embeddings)

print(f"Number of documents indexed: {index.ntotal}")

# Save the FAISS index to a file 
faiss.write_index(index, "candidate_profiles.index")

# Function to search the FAISS index
def search_faiss(query, model, index, top_k=5):
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype='float32')
    distances, indices = index.search(query_embedding, top_k)
    return distances, indices

# Example usage
if __name__ == "__main__":
    query = "Data scientist with experience in machine learning"
    distances, indices = search_faiss(query, model, index)
    
    print(f"Top {len(indices[0])} matches:")
    for idx, dist in zip(indices[0], distances[0]):
        print(f"Document: {data[idx]} \nDistance: {dist}\n")


# Works well, now that we have index, we need to finetune an LLM,
# integrate RAG and build a UI