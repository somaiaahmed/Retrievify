from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums, DocumentTypeEnum
import cohere
import logging


class CoHereProvider(LLMInterface):
    """
    Implementation of the LLMInterface using CoHere's API.
    This class provides methods to interact with CoHere's models for text generation and embedding.
    """
    
    def __init__(self, api_key: str,
                    default_input_max_characters: int = 1000,
                    default_generation_max_output_token: int = 1000,
                    default_generation_temperature: float = 0.1):

        self.api_key = api_key
        
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_token = default_generation_max_output_token
        self.default_generation_temperature = default_generation_temperature    
        
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None
        
        self.client = cohere.Client(
            api_key=self.api_key,
        )
        
        self.logger = logging.getLogger(__name__)
        
    
    def set_genertion_model(self, model_id: str):
        self.generation_model_id = model_id
    
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def process_text(self, text: str):
        
        return text[:self.default_input_max_characters].strip()
    
    def generate_text(self, prompt: str, chat_history: list, max_output_token: int=None,
                      temperature: float = None):
        
        if not self.client:
            self.logger.error("CoHere client is not initialized.")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model for CoHere is not set.")
            return None
        
        max_output_token = max_output_token if max_output_token else self.default_generation_max_output_token
        temperature = temperature if temperature else self.default_generation_temperature
        
        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message=self.process_text(prompt),
            temperature=temperature,
            max_tokens=max_output_token
        )
        
        if not response or not response.text:
            self.logger.error("Failed to get response from CoHere API.")
            return None
        
        return response.text
    
    def embed_text(self, text: str, document_type: str = None):
        
        if not self.client:
            self.logger.error("CoHere client is not initialized.")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for CoHere is not set.")
            return None
        
        input_type = CoHereEnums.DOCUMENT
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = CoHereEnums.QUERY
        
        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type.value,
            embedding_types=['float']
        )
        
        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Failed to get embedding from OpenAI API.")
            return None
        
        return response.embeddings.float[0]
    
    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "text": self.process_text(prompt)
        }