from enum import Enum

from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum


class SpeakerType(Enum):
    HOST = "host"
    GUEST = "guest"


@dataclass
class Message:
    speaker: str
    speaker_type: SpeakerType
    content: str
    timestamp: str
    turn_number: int


@dataclass
class PodcastState:
    messages: List[Message]
    current_turn: int
    current_speaker: str
    topic: str
    participants: Dict[str, Any]
    is_finished: bool
    max_turns: int = 10


class AIModelEnum(Enum):
    OPENAI = "OPENAI"
    GOOGLE = "GOOGLE"


class EnvEnum(Enum):
    DEV = "DEV"
    STAGE = "STAGE"
    PRODUCTION = "PRODUCTION"
