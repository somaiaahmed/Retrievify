from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import (DistanceMethodEnums, PgVectorTableShemeEnums,
                             PgVectorDistanceMethodEnums, PgVectorIndexTypeEnums)
import logging
from typing import List
from models.db_schemes import RetrievedDocument 
from sqlalchemy.sql import text as sql_text
import json

class PGVectorProvider(VectorDBInterface):
    
    def __init__(self, db_client: str, default_vector_size: int = 786,
                 distance_method: str = None, index_treshold: int = 100):

        self.db_client = db_client
        self.default_vector_size = default_vector_size
        self.distance_method = distance_method
        self.index_treshold = index_treshold

        self.pgvector_table_prefix = PgVectorTableShemeEnums._PREFIX.value
        
        self.logger = logging.getLogger("uvicorn")
        self.default_index_name = lambda collection_name: f"{collection_name}_vector_idx"


    async def connect(self):
        """
        Connect to the PGVector database.
        """
        async with self.db_client() as session:
            async with session.begin():
                await session.execute(
                    sql_text(
                        "CREATE EXTENSION IF NOT EXISTS vector"
                    )
                )
                await session.commit()
            
    async def disconnect(self):
        """
        Disconnect from the PGVector database.
        """
        pass
    
    async def is_collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists in the PGVector database.
        """
        record = None
        async with self.db_client() as session:
            async with session.begin():
                list_tbl = sql_text("SELECT * FROM pg_tables WHERE tablename = :collection_name")
                results = await session.execute(list_tbl, {"collection_name": collection_name})
                record = results.scalar_one_or_none()
                
            return record

    async def list_all_collections(self) -> List[str]:
        """
        List all collections in the PGVector database.
        """
        records = []
        async with self.db_client() as session:
            async with session.begin():
                list_tbl = sql_text("SELECT tablename FROM pg_tables WHERE tablename LIKE :prefix")
                results = await session.execute(list_tbl, {"prefix": self.pgvector_table_prefix})
                records = [row[0] for row in results.fetchall()]

        return records
    
    async def get_collection_info(self, collection_name: str) -> dict:
        """
        Get information about a specific collection in the PGVector database.
        """
        record = None
        async with self.db_client() as session:
            async with session.begin():
                table_info_sql = sql_text(''' 
                    SELECT tablename, schemaname, tableowner, tablespace, hasindexes, hasrules, hastriggers
                    FROM pg_tables
                    WHERE tablename = :collection_name
                ''')
                count_sql = sql_text('SELECT COUNT(*) FROM :collection_name')
                table_info = await session.execute(table_info_sql, {"collection_name": collection_name})
                record_count = await session.execute(count_sql, {"collection_name": collection_name})
                
                table_data = table_info.fetchone()
                if not table_data:
                    return None
                
                return{
                    "table_info": dict(table_data),
                    "record_count": record_count
                }

    async def delete_collection(self, collection_name: str):
        """
        Delete a collection from the PGVector database.
        """
        async with self.db_client() as session:
            async with session.begin():
                self.logger.info(f"Deleting collection: {collection_name}")

                drop_table = sql_text(f"DROP TABLE IF EXISTS {collection_name} CASCADE")
                await session.execute(drop_table, {"collection_name": collection_name})
                await session.commit()
            
        return True
    

    async def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False):
        """
        Create a new collection in the PGVector database.
        """
        if do_reset:
           _ = await self.delete_collection(collection_name)
        
        is_collection_exists = await self.is_collection_exists(collection_name)
        if not is_collection_exists:
            self.logger.info(f"Creating collection {collection_name}.")
            
            async with self.db_client() as session:
                async with session.begin():
                    create_table_sql = sql_text(f'''
                        CREATE TABLE IF NOT EXISTS {collection_name} (
                        {PgVectorTableShemeEnums.ID.value} bigserial PRIMARY KEY,
                        {PgVectorTableShemeEnums.TEXT.value} text,
                        {PgVectorTableShemeEnums.VECTOR.value} vector({embedding_size}),
                        {PgVectorTableShemeEnums.METADATA.value} JSONB DEFAULT '{{}}',
                        {PgVectorTableShemeEnums.CHUNK_ID.value} integer,
                        forigen key ({PgVectorTableShemeEnums.CHUNK_ID.value}) references chunks(chunk_id) 
                    )
                ''')
                await session.execute(create_table_sql)
                await session.commit()
        
            return True
        
        return False
    
    async def is_index_exists(self, collection_name: str, index_name: str = None) -> bool:
        """
        Check if an index exists in the PGVector collection.
        """
        
        index_name = self.default_index_name(collection_name)
        
        async with self.db_client() as session:
            async with session.begin():
                check_sql = sql_text('''
                    SELECT * FROM pg_indexes 
                    WHERE tablename = :collection_name 
                    AND indexname = :index_name
                ''')
                result = await session.execute(check_sql, {
                    "collection_name": collection_name,
                    "index_name": index_name
                })
                return bool(result.scalar_one_or_none())
    
    
    async def create_vector_index(self, collection_name: str,
                           index_type: str = PgVectorIndexTypeEnums.HNSW.value,): 
        """
        Create an index for the PGVector collection.
        """
        
        is_index_exists = await self.is_index_exists(collection_name)
        if is_index_exists:
            return False
        
        async with self.db_client() as session:
            async with session.begin():
                count_sql = sql_text(f'SELECT COUNT(*) FROM {collection_name}')
                result = await session.execute(count_sql)
                records_count = result.scalar_one()
                
                if records_count < self.index_treshold:
                    return False
                
                self.logger.info(f"Start creating index for {collection_name} with type {index_type}.")
                
                index_name = self.default_index_name(collection_name)
                create_index_sql = sql_text(f'''
                    CREATE INDEX IF NOT EXISTS {index_name}
                    ON {collection_name} USING {index_type} ({PgVectorTableShemeEnums.VECTOR.value} 
                    {self.distance_method})
                ''')
                await session.execute(create_index_sql)

                self.logger.info(f"End creating index for {collection_name} with type {index_type}.")
        
        
    async def reset_vector_index(self, collection_name: str,
                                 index_type: str = PgVectorIndexTypeEnums.HNSW.value):
        """
        Reset the vector index for the PGVector collection.
        """
        index_name = self.default_index_name(collection_name)

        async with self.db_client() as session:
            async with session.begin():
                drop_index_sql = sql_text(f'DROP INDEX IF EXISTS {index_name}')
                await session.execute(drop_index_sql)

        return await self.create_vector_index(
            collection_name=collection_name,
            index_type=index_type
        ) 

    async def insert_one(self, collection_name: str, text: str, vector: list,
                        metadata: dict = None,
                        record_id: str = None):
        """
        Insert a single record into the PGVector collection.
        """
        is_collection_exists = await self.is_collection_exists(collection_name)
        if not is_collection_exists:
            self.logger.info(f"Can not insert record into {collection_name} because it does not exist.")
            return False

        if not record_id:
            self.logger.info(f"Record ID is not provided for insertion into {collection_name}.")
            return False
        
        async with self.db_client() as session:
            async with session.begin():
                insert_sql = sql_text(f'''
                    INSERT INTO {collection_name} (
                    {PgVectorTableShemeEnums.TEXT.value}, 
                    {PgVectorTableShemeEnums.VECTOR.value},
                    {PgVectorTableShemeEnums.METADATA.value}, 
                    {PgVectorTableShemeEnums.CHUNK_ID.value})
                    VALUES (:text, :vector, :metadata, :chunk_id)
                ''')
                
                await session.execute(insert_sql, {
                    "text": text,
                    "vector": "[" + ",".join([str(v) for v in vector]) + "]",
                    "metadata": metadata,
                    "chunk_id": record_id
                })
                await session.commit()
        
        return True
    
    
    async def insert_many(self, collection_name: str, texts: list,
                        vectors: list, metadata: list = None,
                        record_ids: list = None, batch_size: int = 50):
        """ Insert many records into the PGVector collection.
        """
        is_collection_exists = await self.is_collection_exists(collection_name)
        if not is_collection_exists:
            self.logger.info(f"Can not insert record into {collection_name} because it does not exist.")
            return False

        if len(vectors) != len(record_ids):
            self.logger.error("Vectors and record IDs must have the same length.")
            return False
        
        if not metadata or len(metadata) == 0:
            metadata = [None] * len(texts)

        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(texts), batch_size):
                    batch_texts = texts[i:i + batch_size]
                    batch_vectors = vectors[i:i + batch_size]
                    batch_metadata = metadata[i:i + batch_size] if metadata else [None] * len(batch_texts)
                    batch_record_ids = record_ids[i:i + batch_size]
                    
                    values = []

                    for _text, _vector, _metadata, _record_id in zip(batch_texts, batch_vectors, batch_metadata, batch_record_ids):
                        values.append({
                            "text": _text,
                            "vector": "[" + ",".join([str(v) for v in _vector]) + "]",
                            "metadata": _metadata,
                            "chunk_id": _record_id
                        })
                    
                    batch_insert_sql = sql_text(f'''
                        INSERT INTO {collection_name} (
                        {PgVectorTableShemeEnums.TEXT.value}, 
                        {PgVectorTableShemeEnums.VECTOR.value},
                        {PgVectorTableShemeEnums.METADATA.value}, 
                        {PgVectorTableShemeEnums.CHUNK_ID.value})
                        VALUES (:text, :vector, :metadata, :chunk_id)
                        ON CONFLICT ({PgVectorTableShemeEnums.ID.value}) DO NOTHING
                    ''')
                    await session.execute(batch_insert_sql, values)
        return True
 
    async def search_by_vector(self, collection_name: str, vector: list, limit: int = 10) -> List[RetrievedDocument]:
        """
        Search for similar records in the PGVector collection.
        """
        is_collection_exists = await self.is_collection_exists(collection_name)
        if not is_collection_exists:
            self.logger.info(f"Can not search record in {collection_name} because it does not exist.")
            return False
        
        vector = "[" + ",".join([str(v) for v in vector]) + "]"
        
        async with self.db_client() as session:
            async with session.begin():
                search_sql = sql_text(f'''
                           {PgVectorTableShemeEnums.TEXT.value} as text, 
                           1 - ({PgVectorTableShemeEnums.VECTOR.value}, <=> :vector) as score, 
                    FROM {collection_name}
                    ORDER BY score DESC
                    LIMIT {limit}
                ''')
                
                results = await session.execute(search_sql, {"vector": vector})
                records = results.fetchall()
                
        return [
            RetrievedDocument(
                text=record.text,
                score=record.score,
            ) for record in records
        ]
    