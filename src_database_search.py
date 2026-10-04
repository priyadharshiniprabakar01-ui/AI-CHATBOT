from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# ==================================================
# LOAD EMBEDDING MODEL
# ==================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==================================================
# LOAD SRC DATABASE
# ==================================================

vectorstore = Chroma(
    persist_directory="src_database",
    embedding_function=embeddings,
    collection_name="src_website"
)


# ==================================================
# SEARCH SRC DATABASE
# ==================================================

def search_src_database(question, k=5):

    results = vectorstore.similarity_search(
        question,
        k=k
    )

    return results