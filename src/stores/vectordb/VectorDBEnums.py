from enum import Enum

class VectorDBEnum(Enum):
    QDRANT = "qdrant"
    
    
    
class DistanceMethodEnums(Enum):
    COSINE = "cosine"
    DOT = "dot"