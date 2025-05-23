from .llm import OpenAIModel, GoogleModel
from .embeddings import OpenAIEmbedding, GoogleEmbedding
from utils.enums import AIModelEnum
from config.settings import settings


class LLMModelFactory:
    @staticmethod
    def get_model(model_name: str):
        if model_name == AIModelEnum.OPENAI.value:
            return OpenAIModel()
        if model_name == AIModelEnum.GOOGLE.value:
            return GoogleModel()
        else:
            raise ValueError(f"Model {model_name} is not supported")


class EmbeddingModelFactory:
    @staticmethod
    def get_model(model_name: str):
        if model_name == AIModelEnum.OPENAI.value:
            return OpenAIEmbedding()
        if model_name == AIModelEnum.GOOGLE.value:
            return GoogleEmbedding()
        else:
            raise ValueError(f"Model {model_name} is not supported")


llm_model = LLMModelFactory.get_model(settings.DEFAULT_AI_MODEL).get_llm()
embedding_model = EmbeddingModelFactory.get_model(
    settings.DEFAULT_AI_MODEL).get_embedding()
