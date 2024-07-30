
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders import PyPDFLoader
import pymongo
from utils import move_data_after_saving, upload_s3
from langchain_pinecone import PineconeVectorStore  # for retrieval of vectors
import os
# for generating sentence from vectors
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone  # for pinecone integration / interaction
# for splitting the text
from langchain.text_splitter import RecursiveCharacterTextSplitter
# for loading the files
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
import warnings  # for ignoring warnings
warnings.filterwarnings("ignore")
uri = 'mongodb+srv://jawadkhan10322:SJeA4BwzDzsbJq1x@cluster0.t26noio.mongodb.net/'
client = pymongo.MongoClient(uri)
db = client['islam365']
collection = db['islam365']


model = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')


def get_pdf_content(file_path):

    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_split = RecursiveCharacterTextSplitter(
        chunk_size=1100,
        chunk_overlap=200
    )
    splitted_docs = text_split.split_documents(documents)
    print("splitted ", len(splitted_docs))

    # Extract page number and content from the loaded documents
    pdf_contents = [(i + 1, doc.page_content)
                    for i, doc in enumerate(documents)]

    return len(splitted_docs), splitted_docs, pdf_contents


def create_embeddings(splitted_docs):

    embeddings = model.embed_documents(
        [doc.page_content for doc in splitted_docs])
    print("Created embeddings for", len(embeddings), "documents")
    return embeddings


source = r'C:\Users\HP\OneDrive\Desktop\Islam365online\data'

destination = r'D:\PYTHONLEARNING\100MLDays\data\islamic'


def main():
    list_of_files = os.listdir(
        source)

    for file in list_of_files:
        joined_path = os.path.join(source, file)
        if os.path.isfile(joined_path):

            length, documents, pdf_contents = get_pdf_content(joined_path)
            if length != 0:
                try:
                    embeddings = create_embeddings(documents)
                    for i, (page_num, content) in enumerate(pdf_contents):
                        print(f"Page Number: {page_num}")
                        print(f"Content: {content}")
                        print(f"Embedding: {embeddings[i]}")
                        print("\n" + "="*50 + "\n")
                        document = {
                            "file_name": file,

                            "document_name": os.path.splitext(file)[0],
                            "page_number": page_num,
                            "content": content,

                            "embedding": embeddings[i]
                        }

                        collection.insert_one(document)
                        print(
                            f"Inserted document for page {page_num} of file {file}")
                except Exception as e:
                    continue


if __name__ == "__main__":
    main()
