from .base import BaseModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings


class OpenAIModel(BaseModel):
    def __init__(self):
        self.model = settings.OPENAI_LLM_MODEL

    def get_llm(self):
        return ChatOpenAI(model=self.model)


class GoogleModel(BaseModel):
    def __init__(self):
        self.model = settings.GOOGLE_LLM_MODEL

    def get_llm(self):
        return ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
