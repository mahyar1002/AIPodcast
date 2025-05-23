from .base import BaseEmbedding
from langchain.embeddings.openai import OpenAIEmbeddings
from config.settings import settings


class OpenAIEmbedding(BaseEmbedding):
    def __init__(self):
        self.model = settings.OPENAI_EMBEDDING_MODEL

    def get_embedding(self):
        return OpenAIEmbeddings(model=self.model)


class GoogleEmbedding(BaseEmbedding):
    def __init__(self):
        self.model = "google/embedding-model"

    def get_embedding(self):
        raise NotImplementedError(
            "GoogleEmbedding is not implemented yet."
        )
