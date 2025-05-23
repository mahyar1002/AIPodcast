import json
from typing import List, Dict
from datetime import datetime
from utils.enums import Message, SpeakerType


class ConversationMemory:
    def __init__(self):
        self.conversation_history: List[Message] = []

    def add_message(self, message: Message):
        self.conversation_history.append(message)

    def get_recent_messages(self, count: int = 5) -> List[Message]:
        return self.conversation_history[-count:]

    def get_all_messages(self) -> List[Message]:
        return self.conversation_history

    def save_to_file(self, filename: str):
        data = []
        for msg in self.conversation_history:
            data.append({
                "speaker": msg.speaker,
                "speaker_type": msg.speaker_type.value,
                "content": msg.content,
                "timestamp": msg.timestamp,
                "turn_number": msg.turn_number
            })

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            self.conversation_history = []
            for item in data:
                msg = Message(
                    speaker=item["speaker"],
                    speaker_type=SpeakerType(item["speaker_type"]),
                    content=item["content"],
                    timestamp=item["timestamp"],
                    turn_number=item["turn_number"]
                )
                self.conversation_history.append(msg)
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with empty history.")
