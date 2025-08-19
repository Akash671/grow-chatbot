import os
import json
import faiss
import numpy as np
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer

# --- CONFIGURATION ---
# Load API key from environment variables for security

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

genai.configure(api_key=GOOGLE_API_KEY)

# --- INITIALIZATION ---
app = Flask(__name__)

# Load the pre-trained model for creating embeddings
print("Loading sentence transformer model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the FAISS index and the associated metadata
print("Loading FAISS index and metadata...")
try:
    index = faiss.read_index('.data/grow_app_faq.index')
    with open('.data/metadata.json', 'r') as f:
        metadata = json.load(f)
except FileNotFoundError:
    print("Error: FAISS index or metadata not found. Please run 'create_vector_store.py' first.")
    index = None
    metadata = []

# Configure the Gemini model
generation_config = {
    "temperature": 0.6,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

# --- RAG HELPER FUNCTION ---
def find_most_relevant_solution(query, top_k=1):
    """
    Finds the most relevant solution(s) from the vector store for a given query.
    """
    if index is None:
        return "Sorry, the knowledge base is currently unavailable."

    # Create an embedding for the user's query
    query_embedding = embedding_model.encode([query], convert_to_tensor=False)
    
    # Search the FAISS index for the most similar vectors
    distances, indices = index.search(np.array(query_embedding, dtype='float32'), top_k)
    
    # Retrieve the corresponding solution text
    if indices.size > 0:
        # We only need the top result's solution
        best_index = indices[0][0]
        return metadata[best_index]['solution']
    return None

# --- FLASK ROUTES ---
@app.route('/')
def home():
    """Render the chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle the chat request from the user."""
    data = request.json
    user_query = data.get("message")

    if not user_query:
        return jsonify({"error": "No message provided"}), 400

    # 1. RETRIEVAL step: Find the most relevant context from our data
    retrieved_context = find_most_relevant_solution(user_query)

    if not retrieved_context:
        retrieved_context = "I could not find a specific solution in my knowledge base. Please try rephrasing your question."

    # 2. GENERATION step: Build a prompt for the Gemini model
    prompt = f"""
    You are 'Grow Chatbot', a friendly and professional customer support assistant for the Grow app.
    Your goal is to provide helpful and concise answers to user questions based on the provided context.
    
    **Context from our knowledge base:**
    {retrieved_context}
    
    **User's Question:**
    {user_query}
    
    **Instruction:**
    Based on the context above, answer the user's question in a helpful and clear manner.
    If the context doesn't seem to directly answer the question, politely state that you couldn't find a precise answer and suggest they contact a human agent.
    Do not mention the "context" in your response. Just answer the question directly.
    """

    try:
        # Call the Gemini API
        response = model.generate_content(prompt)
        bot_response = response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        bot_response = "I'm having trouble connecting to my brain right now. Please try again in a moment."

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    # For development, you can run the app directly
    app.run(debug=True, port=5000)