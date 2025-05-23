from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import List, Dict
from models.factory import llm_model


class HostAgent:
    def __init__(self, name: str):
        self.name = name
        self.questions_asked = []

    def generate_opening(self, topic: str, guests: List[str]) -> str:
        """Generate opening statement for the podcast"""

        system_prompt = f"""
        You are {self.name}, a professional podcast host.
        You are hosting a discussion about: {topic}
        
        Your guests are: {', '.join(guests)}
        
        Generate a warm, engaging opening that:
        - Welcomes listeners
        - Introduces the topic
        - Briefly introduces the guests
        - Sets expectations for the discussion
        """

        user_prompt = "Please provide the opening for this podcast episode."

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = llm_model.invoke(messages)
        return response.content

    def generate_question(self, conversation_history: str, guests: List[str], turn_number: int) -> str:
        """Generate a question for the guests"""

        system_prompt = f"""
        You are {self.name}, a professional podcast host.
        
        Your role:
        - Ask engaging questions that promote discussion
        - Keep the conversation balanced
        - Encourage guests to share their perspectives
        - Make sure both guests get opportunities to speak
        
        This is turn {turn_number} of the conversation.
        """

        user_prompt = f"""
        Conversation so far:
        {conversation_history}
        
        Guests: {', '.join(guests)}
        
        Generate your next question or comment to keep the discussion engaging.
        You can either ask a new question or follow up on previous points.
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = llm_model.invoke(messages)
        return response.content

    def generate_closing(self, conversation_history: str) -> str:
        """Generate closing statement for the podcast"""

        system_prompt = f"""
        You are {self.name}, a professional podcast host.
        
        Generate a closing statement that:
        - Summarizes key points from the discussion
        - Thanks the guests
        - Provides a satisfying conclusion
        """

        user_prompt = f"""
        Based on this conversation:
        {conversation_history}
        
        Please provide a closing statement for the podcast.
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = llm_model.invoke(messages)
        return response.content
