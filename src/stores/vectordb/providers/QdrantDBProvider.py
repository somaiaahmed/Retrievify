from qdrant_client import QdrantClient, models
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging
from typing import List

class QdrantDBProvider(VectorDBInterface): 
    
    def __init__(self, db_path: str, distance_method: str):

        self.client = None
        self.db_path = db_path
        self.distance_method = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__)
        
    def connect(self):
        """
        Connect to the QdrantDB.
        """
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        """
        Disconnect from the QdrantDB.
        """
        self.client = None    
        
    def is_collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists in the QdrantDB.
        """
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> List:
        """
        List all collections in the QdrantDB.
        """
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> dict:
        """
        Get information about a specific collection in the QdrantDB.
        """
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str):
        """
        Delete a collection from the QdrantDB.
        """
        if self.is_collection_exists(collection_name): 
            self.client.delete_collection(collection_name=collection_name)

    def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False):
        """
        Create a new collection in the QdrantDB.
        """
        if do_reset:
            _ = self.delete_collection(collection_name=collection_name)
        
        if not self.is_collection_exists(collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method
                )
            )
            
            return True
        
        return False
            
    def insert_one(self, collection_name: str, text: str, vector: list, 
                        metadata: dict = None,
                        record_id: str = None):
        """
        Insert a single record into the QdrantDB collection.
        """
        if not self.is_collection_exists(collection_name):
            self.logger.error("Cannot insert record. Collection does not exist.")
            return False
        
        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[models.Record(
                    id =[record_id],
                    vector=vector,
                    payload={
                        "text": text,
                        "metadata": metadata 
                    }
                )]
            )
        except Exception as e:
            self.logger.error(f"Error inserting record: {e}")
            return False
        
        return True
    
    def insert_many(self, collection_name: str, texts: list,
                        vectors: list, metadata: list = None,
                        record_ids: list = None, batch_size: int = 50):
        """
        Insert many records into the QdrantDB collection.
        """
        if metadata is None:
            metadata = [None] * len(texts)
            
        if record_ids is None:
            record_ids = list(range(0,len(texts)))
            
        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size
            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]
            
            batch_records = [
                models.Record(
                    id=batch_record_ids[x],
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x],
                        "metadata": batch_metadata[x]
                    }
                )
                for x in range(len(batch_texts))
            ]
            
            try:
                _ = self.client.upload_records(
                    collection_name=collection_name, 
                    records=batch_records,
                )
            except Exception as e:
                self.logger.error(f"Error inserting batch: {e}")
                return False
                
        return True 
        
    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):
        """
        Search for records in the VectorDB by vector similarity.
        """
        return self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )
    