import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

# Define the path for the data and the vector store
DATA_FILE_PATH = 'data.json'
VECTOR_STORE_PATH = '.data/grow_app_faq.index'
METADATA_PATH = '.data/metadata.json'

def create_vector_store():
    """
    Reads problem-solution data, generates embeddings for the problems,
    and stores them in a FAISS vector store.
    """
    print("Loading data...")
    try:
        with open(DATA_FILE_PATH, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {DATA_FILE_PATH} not found.")
        return

    # Extract the 'problem' texts to be embedded
    problems = [item['problem'] for item in data]
    
    print("Loading embedding model...")
    # Using a reliable, open-source model for creating embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Generating embeddings for the problems...")
    # The model converts each problem text into a 384-dimensional vector
    embeddings = model.encode(problems, convert_to_tensor=False)
    
    # The dimension of our vectors is 384
    d = embeddings.shape[1]
    
    # Create a FAISS index
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings, dtype='float32'))
    
    print(f"Successfully created a FAISS index with {index.ntotal} vectors.")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
    
    # Save the index and the original data (as metadata)
    faiss.write_index(index, VECTOR_STORE_PATH)
    with open(METADATA_PATH, 'w') as f:
        json.dump(data, f)
        
    print(f"Vector store saved to {VECTOR_STORE_PATH}")
    print(f"Metadata saved to {METADATA_PATH}")

if __name__ == "__main__":
    create_vector_store()