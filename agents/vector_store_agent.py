from qdrant_client import QdrantClient, models
from langchain_community.embeddings import SentenceTransformerEmbeddings
from utils.logger import logger
import pandas as pd


QDRANT_URL = "http://localhost:6333"  
COLLECTION_NAME = "ADP_collection"  

def store_data(df: pd.DataFrame):
    """
    Takes a DataFrame, converts each row to a descriptive sentence,
    and stores it in a Qdrant vector database.
    """
    logger.info("[Vector Store Agent] Preparing data for embedding with Qdrant...")
    
    if df.empty:
        logger.warning("[Vector Store Agent] DataFrame is empty. Skipping embedding.")
        return None

    client = QdrantClient(url=QDRANT_URL)
    
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=384, 
            distance=models.Distance.COSINE
        )
    )
    logger.info(f"Ensured Qdrant collection '{COLLECTION_NAME}' is ready for new data.")

    documents = []
    for index, row in df.iterrows():
        text = ". ".join([f"The {col.replace('_', ' ')} is {val}" for col, val in row.items()])
        documents.append(f"On record {index+1}, {text}.")
        
    embeddings = embedding_function.embed_documents(documents)

    points = []
    for i, (doc, vec) in enumerate(zip(documents, embeddings)):
        points.append(
            models.PointStruct(
                id=i, 
                vector=vec, 
                payload={"document": doc}
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True  
    )
    
    logger.info(f"[Vector Store Agent] Data successfully stored in Qdrant collection '{COLLECTION_NAME}'.")
    return client

