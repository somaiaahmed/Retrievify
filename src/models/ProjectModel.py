from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum 

class ProjectModel(BaseDataModel):
    
    def __init__(self, db_client: object):
        super().__init__(db_client = db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value ]
        
    
        
    async def create_project(self, project: Project):
        """
        Create a new project in the database.
        
        """
        
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project._id = result.inserted_id
        
        return project
    
    async def get_project_or_create_one(self, project_id: str):
        """
        Get a project by its ID or create a new one if it doesn't exist.
        
        """
        
        rec = await self.collection.find_one({
            "project_id": project_id
            })
        
        if rec is None:
            # Create a new project if it doesn't exist
            project = Project(project_id = project_id)
            rec = await self.create_project(project = project)
            
            return project
        
        return Project(**rec)
    
    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        """
        Get all projects from the database.
        
        """
        
        # Count total number of docunments
        total_documents = await self.collection.count_documents({})
        
        # Calculate the number of pages
        total_pages = total_documents // page_size 
        if total_documents % page_size > 0:
            total_pages += 1
            
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        
        projects = []
        async for doc in cursor:
            projects.append(
                Project(**doc)
            )
            
        return projects, total_pages