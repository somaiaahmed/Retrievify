from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum 
from bson.objectid import ObjectId
from pymongo import InsertOne
from sqlalchemy.future import select
from sqlalchemy import func, delete

class ChunkModel(BaseDataModel):
    
    def __init__(self, db_client: object):
        super().__init__(db_client = db_client)
        self.db_client = db_client
        
    
    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Create an instance of ChunkModel and initialize the collection.
        
        """
        
        instance = cls(db_client=db_client)        
        return instance
                
                
    async def create_chunk(self, chunk: DataChunk):
        """
        Create a new chunk in the database.
        
        """
        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.commit()
            await session.refresh(chunk)

        return chunk
        
        
    async def get_chunk(self, chunk_id: str):
        """
        Get a chunk by its ID.
        """
        async with self.db_client() as session:
            query = select(DataChunk).where(DataChunk.id == chunk_id)
            result = await session.execute(query)
            chunk = result.scalar_one_or_none()
            
        return chunk
    
    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        """
        Insert multiple chunks into the database.
        
        """
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i + batch_size]
                    session.add_all(batch)
            await session.commit()
        return len(chunks)
                    
    
    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        """
        Delete all chunks associated with a specific project ID.
        
        """
        async with self.db_client() as session:
            async with session.begin():
                query = delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
                result = await session.execute(query)
                await session.commit()
        return result.rowcount
    
    
    async def get_project_chunks(self, project_id: ObjectId,
                                 page_no: int = 1, page_size: int = 100):
        """
        Get all chunks associated with a specific project.
        
        """
        async with self.db_client() as session:
            async with session.begin():
                query = select(DataChunk).where(DataChunk.chunk_project_id == project_id).offset(
                    (page_no - 1) * page_size
                ).limit(page_size)
                result = await session.execute(query)
                records = result.scalars().all()
            return records

    async def get_total_chunks_count(self, project_id: ObjectId):
        """
        Count the number of chunks associated with a specific project.
        
        """
        total_count = 0
        async with self.db_client() as session:
            count_sql = select(func.count(DataChunk.chunk_id)).where(DataChunk.chunk_project_id == project_id)
            records_count = await session.execute(count_sql)
            total_count = records_count.scalar()
        return total_count