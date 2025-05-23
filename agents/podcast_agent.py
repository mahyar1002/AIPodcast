from typing import List, Dict
from agents.guest_agent import GuestAgent
from agents.host_agent import HostAgent


class PodcastAgent:
    def __init__(self, topic: str, host: HostAgent, guests: List[GuestAgent], max_turns: int = 10):
        self.topic = topic
        self.host = host
        self.guests = guests
        self.max_turns = max_turns
        self.turn_number = 0
        self.conversation_history = []

    def _append_to_history(self, speaker: str, message: str):
        self.conversation_history.append({"role": speaker, "message": message})

    def _format_history(self) -> str:
        return "\n".join([f"{entry['role']}: {entry['message']}" for entry in self.conversation_history])

    def run(self) -> List[Dict[str, str]]:
        # Opening
        opening = self.host.generate_opening(
            self.topic, [guest.name for guest in self.guests])
        self._append_to_history("Host", opening)

        while self.turn_number < self.max_turns:
            self.turn_number += 1

            # Host asks a question
            formatted_history = self._format_history()
            question = self.host.generate_question(
                formatted_history, [g.name for g in self.guests], self.turn_number)
            self._append_to_history("Host", question)

            # Guests respond in order
            for guest in self.guests:
                formatted_history = self._format_history()
                response = guest.generate_response(formatted_history, question)
                self._append_to_history(guest.name, response)

            # Optionally simulate guest-to-guest cross talk (simplified)
            cross_talk = self._generate_cross_talk()
            if cross_talk:
                self._append_to_history("CrossTalk", cross_talk)

        # Closing
        final_history = self._format_history()
        closing = self.host.generate_closing(final_history)
        self._append_to_history("Host", closing)

        return self.conversation_history

    def _generate_cross_talk(self) -> str:
        """Optional: simulate quick back-and-forth between guests (optional, simple version)"""
        if len(self.guests) >= 2:
            guest1, guest2 = self.guests[0], self.guests[1]
            # last host question
            last_question = self.conversation_history[-3]["message"]
            g1 = guest1.generate_response(self._format_history(
            ), f"Respond directly to {guest2.name}'s opinion.")
            g2 = guest2.generate_response(self._format_history(
            ), f"Respond directly to {guest1.name}'s opinion.")
            return f"{guest1.name}: {g1}\n{guest2.name}: {g2}"
        return ""
