from huggingface_hub import InferenceClient  # inference api
import json  # for json formatting
from langchain_pinecone import PineconeVectorStore  # for retrieval of vectors
# for generating sentence from vectors
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone  # for pinecone integration / interaction
import warnings
warnings.filterwarnings("ignore")

# uncomment when want to test LLM only

# # embedding model we are using

# embedding = 'all-mpnet-base-v2'

# print("Embedding model")
# embeddings = SentenceTransformerEmbeddings(model_name=embedding)

# # index connection of of pinecone
# index_name = 'islam365-bert'
# pc = Pinecone(api_key="35590edb-c170-471d-9f8b-f33b89324785")
# print("Pinecone Indexing")
# index = pc.Index(index_name)
# print(index.describe_index_stats())

# # Pinecone Vector Db connection
# print("Pinecone Vector store")
# vectorstore = PineconeVectorStore(index, embedding=embeddings)

API_TOKEN = open('token').read().strip()

# llm connnection
# llm_client = InferenceClient(
#     "mistralai/Mistral-7B-Instruct-v0.3",
#     token=API_TOKEN,
#     timeout=120
# )

# retreiving docs based on query


def retrieval_for_docs(query, vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={'k': 15})
    retrieved_docs = retriever.get_relevant_documents(query)
    return retrieved_docs


def array_format_retrieved_docs(retrieved_docs):

    #################################

    formatted_content = [
        {
            "page": doc.metadata.get('page', 'Unknown'),
            "source": doc.metadata.get('source', 'Unknown').split('/')[-1],
            "content": doc.page_content
        }
        for doc in retrieved_docs
    ]
    return formatted_content
    #################################


def llm_retrieval_response(query, retrieved_documents, llm_client):

    # format to string for llm
    formatted_text = "\n".join([
        f"""
        Page {doc.metadata.get('page', 'Unknown')} - Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}
        """
        for doc in retrieved_documents
    ])
    # print(formatted_text)
    print("--------------------------------")

    # llm prompt design
    input_text = f""" [INST]
        {formatted_text}
        USE THE ABOVE INFORMATION TO GIVE DETAILED ANSWER TO QUESTION BELOW more than (1500 words).
        {query}
        [/INST]"""

    # llm inference request
    response = llm_client.post(
        json={
            "inputs": input_text,
            "parameters": {
                "max_length": 2000,

                "max_new_tokens": 1000,  # giving best at 1000
                "top_k": 25,
                "top_p": 0.9,
                "num_return_sequences": 1,
                "temperature": 1,
                "return_full_text": False,
                "task": "text-generation"
            }
        }
    )
    return json.loads(response.decode())[0]['generated_text']


if __name__ == '__main__':
    query - "islam"
    retrieved_docs = retrieval_for_docs(query, vectorstore)
    formatted_content = array_format_retrieved_docs(retrieved_docs)
    llm_response = llm_retrieval_response(
        query, retrieved_docs, llm_client)
