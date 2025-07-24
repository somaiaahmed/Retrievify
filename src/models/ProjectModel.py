from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum 
from sqlalchemy.future import select
from sqlalchemy import func

class ProjectModel(BaseDataModel):
    
    def __init__(self, db_client: object):
        super().__init__(db_client = db_client)
        self.db_client = db_client
        
    
    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Create an instance of ProjectModel and initialize the collection.
        
        """
        
        instance = cls(db_client=db_client)        
        return instance
    
            
    async def create_project(self, project: Project):
        """
        Create a new project in the database.
        
        """
        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            await session.refresh(project)
            
        return project
        
    
    async def get_project_or_create_one(self, project_id: str):
        """
        Get a project by its ID or create a new one if it doesn't exist.
        
        """
        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = await session.execute(query)
                project = result.scalar_one_or_none()
                if project is None:
                    project_rec = Project(
                        project_id = project_id
                    )
                    project = await self.create_project(project=project_rec)
                    return project
                else:
                    return project                
        
    
    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        """
        Get all projects from the database.
        
        """
        async with self.db_client() as session:
            async with session.begin():
                total_documents = await session.execute(select(
                    func.count(Project.project_id)
                ))
                
                total_documents = total_documents.scalar_one()
                
                total_pages = total_documents // page_size 
                if total_documents % page_size > 0:
                    total_pages += 1
                    
                query = select(Project).offset((page - 1) * page_size).limit(page_size)
                projects = await session.execute(query).scalars().all()

        return projects, total_pages
