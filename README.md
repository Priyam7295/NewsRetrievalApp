# Document-Based Q&A App with LangChain and FAISS
----
## Overview
This app allows users to input documents from internet links, processes the content, and answers user queries based on the most relevant information from the provided documents. It leverages LangChain for document processing and FAISS for fast similarity search.



## Features

- **Document Upload**: Users can provide documents via internet links.
- **Data Processing**: The documents are loaded using `UnstructuredURLLoader` from LangChain, and the content is split into smaller chunks using the `RecursiveTextSplitter`.
- **Embedding**: Each chunk is embedded into vector space for fast similarity matching.
- **Storage**: The embeddings are stored in FAISS for efficient nearest-neighbor searches.
- **Query Handling**: Users can ask questions, which are embedded and then matched against the stored document embeddings to retrieve the most relevant answers.



## Pipeline

This app follows a structured pipeline to process documents and answer user queries:

1. **Document Input**: Users provide URLs linking to the documents they want to process.
2. **Data Loading**: The URLs are passed to the `UnstructuredURLLoader` from LangChain, which extracts the text content from the provided links.
3. **Text Splitting**: The content of the documents is split into smaller, more manageable chunks using the `RecursiveTextSplitter`.
4. **Embedding Creation**: Each chunk is passed through an embedding model (e.g., OpenAI's embeddings) to generate vector representations for each text chunk.
5. **Storing Embeddings**: The generated embeddings are stored in a FAISS index, allowing efficient similarity search.
6. **User Query**: The user inputs a question that needs to be answered.
7. **Query Embedding**: The user's query is embedded into vector space using the same embedding model.
8. **Similarity Search**: The embedded query is compared against the stored embeddings in FAISS to find the most relevant document chunks.
9. **Answer Retrieval**: The most relevant chunk is returned as the answer to the user's query.

Flowchart 


