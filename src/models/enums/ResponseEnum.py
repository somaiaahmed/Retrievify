from enum import Enum

class ResponseSignal(Enum):
    
    FILE_VALIDATED = "File validated successfully."
    FILE_TYPE_NOT_SUPPORTED = "File type is not supported."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit."
    FILE_VALID = "File is valid."
    FILE_UPLOAD_SUCCESS = "File uploaded successfully."
    FILE_UPLOAD_FAILURE = "File upload failed."
   