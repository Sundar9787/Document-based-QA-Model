# Document-based Question Answering using RAG

## 📌 Overview
This project implements a **Retrieval-Augmented Generation (RAG)** pipeline to answer user queries based on custom document datasets.  
The system combines **semantic search** with **generative AI models** to produce context-aware and accurate answers.

## 🚀 Features
- **Document Preprocessing** – Cleans and processes raw documents.
- **Text Chunking** – Splits large documents into manageable chunks for better retrieval.
- **Vector Embeddings** – Uses transformer-based models to convert text into dense vectors.
- **Semantic Search** – Retrieves the most relevant document chunks using a vector database.
- **Answer Generation** – Uses Google’s Gemini 1.5 Flash model for generating accurate responses.
- **RAG Architecture** – Combines retrieval and generation for improved QA performance.

## 🛠️ Tech Stack
- **Python 3.10+**
- **Transformers** (Hugging Face)
- **SentenceTransformers**
- **Google Generative AI SDK**
- **FAISS** (for vector storage & retrieval)
- **Pandas, NumPy**
  

```

## ⚙️ How It Works
1. **Document Ingestion** – Load and preprocess documents (PDF, TXT, DOCX, etc.).
2. **Text Chunking** – Break documents into smaller, overlapping segments.
3. **Embedding Generation** – Convert chunks into vector embeddings.
4. **Vector Storage** – Store embeddings in a vector database for quick retrieval.
5. **Query Handling** – Convert the user’s question into an embedding.
6. **Relevant Context Retrieval** – Find top-N chunks most relevant to the query.
7. **Answer Generation** – Pass the retrieved context + query to a generative model.
8. **Output** – Display a final, contextually accurate answer.

## 📊 Example
**Query:** *"What are the key features of the project?"*  
**Answer:** *"The project uses a Retrieval-Augmented Generation architecture with semantic search, text chunking, and generative AI to answer document-based queries accurately."*

## 📈 Results
- Improved **accuracy** and **context relevance** compared to keyword-based search.
- Handles **long documents** efficiently with chunking and semantic embeddings.
- Provides **human-like responses** with minimal hallucination.

## ▶️ Installation & Usage
```bash
# Clone repository
git clone (https://github.com/Sundar9787/Document-based-QA-Model.git)
cd Document-based-QA-Model

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

