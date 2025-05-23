from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from utils.web_scraper import WebScraper
from memory.conversation import ConversationMemory
from typing import Dict, Any
from config.settings import settings
from models.factory import llm_model


class GuestAgent:
    def __init__(self, name: str, company: str, characteristics: str):
        self.name = name
        self.company = company
        self.characteristics = characteristics
        self.web_scraper = WebScraper(company)
        self.company_knowledge = self._gather_company_knowledge()

    def _gather_company_knowledge(self) -> str:
        """Gather knowledge about the company from web sources"""
        company_info = self.web_scraper.get_info()
        # recent_news = self.web_scraper.get_news(self.company)

        knowledge = f"""
        Company Information for {self.company}:
        {company_info.get("content", "No summary available.")}
        """
        return knowledge

    def generate_response(self, conversation_history: str, current_context: str) -> str:
        """Generate a response based on conversation history and context"""

        system_prompt = f"""
        You are {self.name}, a representative from {self.company}.
        
        Your characteristics: {self.characteristics}
        
        Your company knowledge:
        {self.company_knowledge}
        
        Instructions:
        - Stay in character as someone who works for {self.company}
        - Promote {self.company} naturally in conversation
        - Use your company knowledge to make informed points
        - Be conversational and engaging
        - Respond to other participants appropriately
        - Keep responses concise (2-3 sentences max)
        """

        user_prompt = f"""
        Conversation so far:
        {conversation_history}
        
        Current context: {current_context}
        
        Please respond as {self.name} from {self.company}:
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = llm_model.invoke(messages)
        return response.content
