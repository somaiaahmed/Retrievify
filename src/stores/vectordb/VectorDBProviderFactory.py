from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBEnum
from controllers.BaseController import BaseController

class VectorDBProviderFactory:
    """
    Factory class to create vector database provider instances.
    """
    
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()
        
    def create(self, provider: str):
        """
        Create a vector database provider instance based on the provider type.
            
        """
        if provider == VectorDBEnum.QDRANT.value:
            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
            return QdrantDBProvider(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD
            )
       
        return None  