# Loading libraries
import langchain
from langchain.document_loaders import TextLoader
import pandas as pd
import numpy as np
from langchain.document_loaders import TextLoader
import getpass
import time
import pickle
from langchain_mistralai import ChatMistralAI
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import faiss
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.title("News Research Tool")
st.sidebar.title("News Article URLs")

# 3 URLs
file_path = "faiss_store.pkl"

# For loading UI
main_placeholder = st.empty()

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

urls = []
for i in range(2):
    url = st.sidebar.text_input(f"URL {i + 1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Load Documents")

if process_url_clicked:
    # 1. Loading the URL in data
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data Loading ....")
    data = loader.load()

    # 2. Creating chunks using RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        # Where it breaks
        separators=["\n\n", "\n", ".", ","],
        chunk_size=1000,
        chunk_overlap=0
    )

    main_placeholder.text("Text splitter started ....")
    docs = text_splitter.split_documents(data)

    # 3. Creating Embedding AND SAVING IT TO FAISS index
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    vector_index = FAISS.from_documents(docs, embeddings)
    main_placeholder.text("Embedding vector started building ....")
    time.sleep(2)

    # Save the FAISS index to a pickle file
    with open(file_path, "wb") as f:
        pickle.dump(vector_index, f)

query = main_placeholder.text_input("Question: ")

if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)
            
            # Modify the retriever to fetch only the closest 3 documents
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            
            # Use the retriever and the LLM to create the retrieval chain
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=retriever)
            langchain.debug = True
            result = chain({"question": query}, return_only_outputs=True)
            
            st.header("Answer")
            st.write(result["answer"])

            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")  # Split the sources by newline
                for source in sources_list:
                    st.write(source)
