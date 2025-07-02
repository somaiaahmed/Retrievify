from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import os

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024 # 1 MB in bytes
        
    def validate_uploaded_file(self, file: UploadFile):
        """
        Validate the uploaded file based on allowed extensions and size.
        """
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:  # Convert MB to bytes
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED.value
    
    def generate_uniqie_filename(self, orig_file_name: str, project_id: str):
        """
        Generate the file name for the uploaded file.
        """
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        
        cleaned_file_name = self.get_clean_filename(
            orig_file_name = orig_file_name
        )
        
        new_file_path = os.path.join(
            project_path,
            f"{random_key}_{cleaned_file_name}"
        )
        
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                f"{random_key}_{cleaned_file_name}"
            )
            
        return new_file_path
    
    
    def get_clean_filename(self, orig_file_name: str):
        
        # remove any special characters.
        cleaned_file_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', orig_file_name)
        
        # replace space with underscore.
        cleaned_file_name = cleaned_file_name.replace(' ', '_')
        
        return cleaned_file_name