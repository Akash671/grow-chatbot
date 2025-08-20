# grow-chatbot
grow chatbot for customer support
# Grow Chatbot (RAG + Gemini 1.5 Flash)

This is a customer support chatbot for the "Grow" app, built using a Retrieval-Augmented Generation (RAG) architecture. It uses a Python Flask backend, a FAISS vector store for retrieval, and Google's Gemini 1.5 Flash model for generation.

## Features

-   **RAG Architecture**: Retrieves relevant information from a knowledge base (`data.json`) before generating a response.
-   **Gemini 1.5 Flash**: Utilizes a fast and powerful LLM for natural and accurate conversations.
-   **Flask Backend**: A lightweight and robust web server.
-   **Attractive UI**: A clean and modern chat interface built with HTML, CSS, and JavaScript.
-   **Easy to Deploy**: Ready to be deployed on platforms like Render or Hugging Face Spaces.

## How It Works

1.  **Indexing**: The `create_vector_store.py` script reads the `data.json` file, converts the "problem" descriptions into numerical vectors (embeddings), and stores them in a FAISS index.
2.  **Retrieval**: When a user asks a question, the backend converts the query into an embedding and uses FAISS to find the most similar (i.e., most relevant) problem-solution pair from the indexed data.
3.  **Generation**: The retrieved solution is passed as "context" to the Gemini 1.5 Flash model along with the original user query. The LLM then generates a helpful, conversational answer based on this context.

## Setup and Running Locally

### Prerequisites

-   Python 3.8+
-   Git

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd grow-chatbot
python -m flask run
got to http://127.0.0.1:5000/
start using...
