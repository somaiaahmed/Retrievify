from pydantic import BaseModel, field, Validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunk_text: str = field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = field(..., gt=0)
    chunk_project_id: ObjectId
    
    
    class Config:
        arbitrary_types_allowed = True
       