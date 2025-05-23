from .base import BaseModel
from langchain_openai import ChatOpenAI
from config.settings import settings


class OpenAIModel(BaseModel):
    def __init__(self):
        self.model = settings.OPENAI_LLM_MODEL

    def get_llm(self):
        return ChatOpenAI(model=self.model)


class GoogleModel(BaseModel):
    def __init__(self):
        self.model = "google/embedding-model"

    def get_llm(self):
        raise NotImplementedError(
            "GoogleModel is not implemented yet."
        )
