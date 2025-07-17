import json
from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List

class NLPController(BaseController):
    """
    NLPController is responsible for handling NLP-related operations.
    It extends the BaseController to inherit common functionalities.
    """

    def __init__(self, vectordb_client, generation_client, embedding_client):
        super().__init__()
        
        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        
    def create_collection_name(self, project_id: str) -> str:
        """
        Creates a collection name based on the project ID.
        """
        return f"collection_{project_id}".strip()
    
    def reset_vectordb_collection(self, project: Project):
        """
        Resets the vector database collection for the given project.
        """
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vectordb_collection_info(self, project: Project):
        """
        Retrieves information about the vector database collection for the given project.
        """
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)
        
        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def index_into_vectordb(self, project: Project, chunks: List[DataChunk],
                            chunks_ids: List[int],
                            do_reset: bool = False):
        """
        Indexes the provided data into the vector database for the given project.
        """
       
        # step 1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)
        
        # step 2: manage items
        texts = [
            c.chunk_text for c in chunks
        ]
        
        metadata = [
            c.chunk_metadata for c in chunks
        ]
        
        vectors = [
            self.embedding_client.embed_text(text=text,
                                             document_type=DocumentTypeEnum.DOCUMENT.value) 
            for text in texts
        ]
        
        # step3: create collection if not exists
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )
        
        # step 4: insert into vectordb
        _ = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )
        
        return True
    
    def search_vectordb_collection(self, project: Project, text: str, limit: int = 10):
        """
        Searches the vector database collection for the given project using the provided text.
        """
        collection_name = self.create_collection_name(project_id=project.project_id)
        
        # step 1: embed the search text
        vector = self.embedding_client.embed_text(
            text=text,
            document_type=DocumentTypeEnum.QUERY.value
        )
        
        if not vector or len(vector) == 0:
            return False
        
        # step 2: search in vectordb
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )
        
        if not results:
            return False
        
        return json.loads(
            json.dumps(results, default=lambda x: x.__dict__)
        )