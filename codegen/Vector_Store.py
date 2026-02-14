import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_knowledge():
    docs = []
    for file in os.listdir("knowledge"):
        with open(f"knowledge/{file}", "r") as f:
            docs.append(f.read())
    return docs

def build_vectorstore():
    documents = load_knowledge()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    split_docs = splitter.create_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore
