from .providers import QdrantDBProvider, PGVectorProvider
from .VectorDBEnums import VectorDBEnums
from controllers.BaseController import BaseController
from sqlalchemy.orm import SessionMaker

class VectorDBProviderFactory:
    """
    Factory class to create vector database provider instances.
    """
    
    def __init__(self, config, db_client: SessionMaker=None):
        self.config = config
        self.base_controller = BaseController()
        self.db_client = db_client
        
    def create(self, provider: str):
        """
        Create a vector database provider instance based on the provider type.
            
        """
        if provider == VectorDBEnums.QDRANT.value:
            qdrant_db_client = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
            return QdrantDBProvider(
                db_client=qdrant_db_client,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                index_treshold=self.config.VECTOR_DB_PGVEV_INDEX_THRESHOLD
            )
            
        if provider == VectorDBEnums.PGVECTOR.value:
            return PGVectorProvider(
                db_client=self.config.PGVECTOR_DB_CLIENT,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                index_treshold=self.config.VECTOR_DB_PGVEV_INDEX_THRESHOLD
            )
       
        return None  