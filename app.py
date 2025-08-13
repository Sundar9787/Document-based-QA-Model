import streamlit as st
from utils import load_docs, break_docs, make_store, ask_gemini

st.set_page_config(page_title="RAG APP")

st.title("Retrieval Augmented Generation (RAG) Application")
st.write("Upload PDFs, Word docs or text files and ask questions about them.")

# session state to keep vector store
if "store" not in st.session_state:
    st.session_state.store = None

# file upload
st.sidebar.header("Upload Files")
files = st.sidebar.file_uploader(
    "Pick your files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# process button
if files:
    if st.sidebar.button("Process"):
        with st.spinner("Reading files..."):
            docs = load_docs(files)
            if len(docs) == 0:
                st.error("No text found in files")
            else:
                parts = break_docs(docs)
                if len(parts) == 0:
                    st.error("Could not split docs into chunks")
                else:
                    st.session_state.store = make_store(parts)
                    if st.session_state.store:
                        st.success("Files uploaded now ask questions!")

# question input
st.subheader("Ask a Question")
q = st.text_input("Your question:")

if st.button("Ask"):
    if q.strip() == "":
        st.warning("Type something first.")
    elif st.session_state.store is None:
        st.error("Please upload and process docs first.")
    else:
        with st.spinner("Thinking..."):
            ans = ask_gemini(st.session_state.store, q)
            st.write("**Answer:**", ans)
