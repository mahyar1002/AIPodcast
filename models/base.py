from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def get_llm(self):
        pass

class BaseEmbedding(ABC):
    @abstractmethod
    def get_embedding(self):
        pass