from abc import ABC, abstractmethod

class LLMInterface(ABC):
    """
    Abstract base class for a Large Language Model (LLM) interface.
    This class defines the methods that any LLM implementation must provide.
    """
    
    @abstractmethod
    def set_genertion_model(self, model_id: str):
        """
        Set the generation model to be used by the LLM.
        """
        pass
    
    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        """
        Set the embedding model to be used by the LLM.
        """
        pass
    
    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list, max_output_token: int, 
                            temperature: float =None):
        """
        Generate text based on the provided prompt.
        """
        pass
    
    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):
        """
        Embed the provided text for semantic search or other purposes.
        """
        pass
    
    @abstractmethod
    def construct_prompt(self, prompt: str. role: str):
        """
        Construct a prompt with the specified role.
        """
        pass