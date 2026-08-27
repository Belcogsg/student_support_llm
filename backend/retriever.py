import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


BACKEND_DIR = Path(__file__).parent
PDF_FILE = BACKEND_DIR / "almanac.pdf"
DB_DIR = BACKEND_DIR / "faiss_index"

def load_or_create_vectorstore():
    """Builds a FAISS index from the PDF if it doesn't exist, or loads existing index from disk."""
    embeddings = OpenAIEmbeddings()

    
    if DB_DIR.exists():
        return FAISS.load_local(
            str(DB_DIR), 
            embeddings, 
            allow_dangerous_deserialization=True
        )

    if not PDF_FILE.exists():
        raise FileNotFoundError(f"Almanac file not found at: {PDF_FILE}")

    
    loader = PyPDFLoader(str(PDF_FILE))
    documents = loader.load()

    # here im splitting the document into searchable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    # creating the FAISS vector database and saving to disk
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(str(DB_DIR))
    
    return vectorstore


_vectorstore = load_or_create_vectorstore()
_retriever = _vectorstore.as_retriever(search_kwargs={"k": 4})

def retrieve_context(question: str) -> str:
    """Retrieves top 4 relevant passages from the UDSM PDF for a given question."""
    docs = _retriever.invoke(question)
    
    # Combines content with page numbers for transparency
    context_blocks = []
    for doc in docs:
        page_num = doc.metadata.get("page", 0) + 1
        context_blocks.append(f"[Page {page_num}]\n{doc.page_content}")

    return "\n\n---\n\n".join(context_blocks)