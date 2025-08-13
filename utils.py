import os
import tempfile
from pathlib import Path
from typing import List
import asyncio

# google generative ai sdk
import google.generativeai as genai
from dotenv import load_dotenv

# langchain stuff
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# load the API key from .env
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_KEY is None:
    raise Exception("Gemini API key not found! Put it in .env as GEMINI_API_KEY")

# tell gemini the key
genai.configure(api_key=GEMINI_KEY)

# function to load all files user uploads
def load_docs(uploaded_files) -> List:
    all_texts = []
    for f in uploaded_files:
        ext = Path(f.name).suffix.lower()

        # save file in temp folder
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file.write(f.read())
            path = temp_file.name

        # pick loader depending on type
        if ext == ".pdf":
            loader = PyPDFLoader(path)
        elif ext == ".docx":
            loader = Docx2txtLoader(path)
        elif ext == ".txt":
            loader = TextLoader(path, encoding="utf-8")
        else:
            print("Skipping file:", f.name)
            continue

        # load and append
        docs = loader.load()
        all_texts.extend(docs)

    return all_texts


# break documents into chunks
def break_docs(docs: List, size: int = 1000, overlap: int = 200) -> List:
    if len(docs) == 0:
        print("No docs to split")
        return []
    splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    chunks = splitter.split_documents(docs)
    return chunks


# make vector store with embeddings
def make_store(chunks: List):
    if len(chunks) == 0:
        print("No chunks given")
        return None

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    embedder = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GEMINI_KEY
    )

    store = FAISS.from_documents(chunks, embedder)
    return store


# run query on vector store and use gemini to answer
def ask_gemini(store, question: str, k: int = 3) -> str:
    if store is None:
        return "No data to search in."

    retriever = store.as_retriever(search_kwargs={"k": k})
    docs = retriever.get_relevant_documents(question)

    context = ""
    for d in docs:
        context += d.page_content + "\n\n"

    # make a simple prompt
    prompt = f"Use this info to answer:\n{context}\nQuestion: {question}\nAnswer:"

    model = genai.GenerativeModel("gemini-1.5-flash")
    reply = model.generate_content(prompt)
    return reply.text
