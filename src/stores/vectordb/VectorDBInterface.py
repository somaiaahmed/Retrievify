from abc import ABC, abstractmethod
from typing import List

class VectorDBInterface(ABC):
    """
    Abstract base class for a Vector Database (VectorDB) interface.
    This class defines the methods that any VectorDB implementation must provide.
    """

    @abstractmethod
    def connect(self):
        """
        Connect to the VectorDB.
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """
        Disconnect from the VectorDB.
        """
        pass
    
    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists in the VectorDB.

        """
        pass
    
    @abstractmethod
    def list_all_collections(self) -> List:
        """
        List all collections in the VectorDB.
        """
        pass
    
    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        """
        Get information about a specific collection in the VectorDB.
        """
        pass
    
    @abstractmethod
    def delete_collection(self, collection_name: str):
        """
        Delete a collection from the VectorDB.
        """
        pass
    
    @abstractmethod
    def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False):
        """
        Create a new collection in the VectorDB.

        """
        pass
    
    @abstractmethod
    def insert_one(self, collection_name: str, text: str, vector: list,
                        metadata: dict = None,
                        record_id: str = None):
        """
        Insert a single record into the VectorDB.
        """
        pass
    
    @abstractmethod
    def insert_many(self, collection_name: str, texts: list,
                        vectors: list, metadata: list = None,
                        record_ids: list = None, batch_size: int = 50):
        """
        Insert many records into the VectorDB.
        """
        pass
    
    @abstractmethod
    def search_by_vector(self, collection_name: str, vector: list, limit: int = 10):
        """
        Search for records in the VectorDB by vector similarity.
        """
        pass
    