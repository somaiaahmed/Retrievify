from enum import Enum

class ResponseSignal(Enum):
    
    FILE_VALIDATED = "File validated successfully."
    FILE_TYPE_NOT_SUPPORTED = "File type is not supported."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit."
    FILE_VALID = "File is valid."
    FILE_UPLOAD_SUCCESS = "File uploaded successfully."
    FILE_UPLOAD_FAILURE = "File upload failed."
    PROCESSING_FAILED = "File processing failed."
    PROCESSING_SUCCESS = "File processed successfully."
    NO_FILES_ERROR = "No files found."
    FILE_ID_ERROR = "NO File found with this id."
    PROJECT_NOT_FOUND_ERROR = "Project not found."
    INSERT_INTO_VECTORDB_ERROR = "Error inserting data into the database."
    INSERT_INTO_VECTORDB_SUCCESS = "Data inserted into the vector database successfully."
    VECTORDB_COLLECTION_RETRIEVED = "Vector database collection retrieved successfully."
    VECTORD_SEARCH_SUCCESS = "Vector database search completed successfully."
    VECTORD_SEARCH_ERORR = "Vector database search failed."
   