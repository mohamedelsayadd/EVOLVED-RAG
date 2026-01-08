from ..LLMInterface import LLMInterface
from ..LLMEnums import GeminiEnums
import google.generativeai as genai
import logging

class GeminiProvider(LLMInterface):

    def __init__(self, api_key: str,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
        
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None 
        self.embedding_model_id = None
        self.embedding_size = None
        
        self.enums = GeminiEnums

        genai.configure(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        
        if not self.generation_model_id:
            self.logger.error("Generation model for Gemini was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        # Process chat history
        gemini_history = []
        system_instruction = None

        for msg in chat_history:
            role = msg.get("role")
            content = msg.get("content")

            if role == self.enums.SYSTEM.value:
                system_instruction = content
            elif role == self.enums.USER.value:
                gemini_history.append({"role": "user", "parts": [content]})
            elif role == self.enums.ASSISTANT.value:
                gemini_history.append({"role": "model", "parts": [content]})

        # Add current prompt
        gemini_history.append({"role": "user", "parts": [prompt]})
        
        # Initialize model with system instruction if present
        if system_instruction:
            model = genai.GenerativeModel(
                model_name=self.generation_model_id,
                system_instruction=system_instruction
            )
        else:
            model = genai.GenerativeModel(self.generation_model_id)

        try:
            response = model.generate_content(
                gemini_history,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_output_tokens,
                    temperature=temperature
                )
            )

            if not response.text:
                self.logger.error("Gemini returned empty text or blocked response")
                return None

            return response.text

        except Exception as e:
            self.logger.error(f"Error while generating text with Gemini: {e}")
            return None


    def embed_text(self, text: str | list[str], document_type: str = None):
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for Gemini was not set")
            return None
        
        if isinstance(text,str):
            text = [text]
        
        embeddings = []
        for t in text:
            try:
                # task_type mapping
                task_type = "retrieval_document" if document_type == "document" else "retrieval_query"
                
                response = genai.embed_content(
                    model=self.embedding_model_id,
                    content=t,
                    task_type=task_type
                )
                
                if 'embedding' not in response:
                    self.logger.error("Error embedding text with Gemini: No embedding in response")
                    return None
                    
                embeddings.append(response['embedding'])

            except Exception as e:
                self.logger.error(f"Error while embedding text with Gemini: {e}")
                return None

        return embeddings

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": prompt
        }
