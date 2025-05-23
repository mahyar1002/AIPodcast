from .base import BaseEmbedding
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import settings


class OpenAIEmbedding(BaseEmbedding):
    def __init__(self):
        self.model = settings.OPENAI_EMBEDDING_MODEL

    def get_embedding(self):
        return OpenAIEmbeddings(model=self.model)


class GoogleEmbedding(BaseEmbedding):
    def __init__(self):
        self.model = settings.GOOGLE_EMBEDDING_MODEL

    def get_embedding(self):
        return GoogleGenerativeAIEmbeddings(
            model=self.model,
            google_api_key=settings.GOOGLE_API_KEY,
            task_type="retrieval_document",
        )
