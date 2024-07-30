import google.generativeai as genai
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from RAG.LLM import retrieval_for_docs, array_format_retrieved_docs, llm_retrieval_response, API_TOKEN
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import SentenceTransformerEmbeddings
import warnings
from huggingface_hub import InferenceClient  # inference api

app = Flask(__name__)
CORS(app)

# Initialize configurations and models


def initialize_services():
    global vectorstore, llm_client

    # gemini keys
    gemini = 'AIzaSyCnhGHna9kU6-fmolRVc7WdEgehyCOYTSU'
    os.environ['GOOGLE_API_KEY'] = gemini
    genai.configure(api_key=gemini)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Initialize embedding model
    embeddings = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")

    # Pinecone setup
    index_name = 'islam365-bert'
    pc = Pinecone(api_key="35590edb-c170-471d-9f8b-f33b89324785")
    index = pc.Index(index_name)
    vectorstore = PineconeVectorStore(index, embedding=embeddings)

    # Hugging Face client/llm
    llm_client = InferenceClient(
        "mistralai/Mistral-7B-Instruct-v0.3",
        token=API_TOKEN,
        timeout=120
    )


initialize_services()


@app.route('/', methods=['GET', 'POST'])
def home():
    return "Welcome to the RAG API"


@app.route('/rag', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        query = data['query']
        retrieved_docs = retrieval_for_docs(query, vectorstore)
        formatted_content = array_format_retrieved_docs(retrieved_docs)
        llm_response = llm_retrieval_response(
            query, retrieved_docs, llm_client)
        return jsonify({
            'content': formatted_content,
            'result': llm_response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
