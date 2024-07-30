
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


def add_data():
    try:
        os.environ['PINECONE_API_KEY'] = '35590edb-c170-471d-9f8b-f33b89324785'
        index_name = 'islam365-bert'
        pc = Pinecone(api_key="35590edb-c170-471d-9f8b-f33b89324785")
        print("Pinecone Indexing")
        index = pc.Index(index_name)
        print(index.describe_index_stats())

        print("Embedding model")
        embeddings = SentenceTransformerEmbeddings(
            model_name="all-mpnet-base-v2")

        # Uncomment for many files if you have large number of files save in data directory in the explorer and change the glob (format accordingly)
        loader = DirectoryLoader(r'data/',
                                 glob='**/*.pdf', show_progress=True, loader_cls=PyPDFLoader)

        # for single file load the relative loader
        print("pdf loader")
        # loader = PyPDFLoader(r'data\The-Quran-Saheeh-International.pdf')

        print("loading ...")
        docs = loader.load()
        print("total pages ", len(docs))
        print("loaded ...")

        print("splitting ...")

        text_split = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200
        )
        splitted_docs = text_split.split_documents(docs)
        print("splitted ", len(splitted_docs))

        print("saving vectors")
        vectorstore = PineconeVectorStore(
            index_name=index_name, embedding=embeddings)

        vectorstore.add_documents(splitted_docs)

        print("vectors saved successfully")
    except Exception as e:
        print("some error occured", e)


if __name__ == '__main__':
    # add_data()
    move_data_after_saving()
