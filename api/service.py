from agents.host_agent import HostAgent
from agents.guest_agent import GuestAgent
from agents.podcast_agent import PodcastAgent
from .schema import InitiateRequest
from config.settings import settings
import requests
import io


async def initiate_agents(params: InitiateRequest):
    host = HostAgent(name=params.host.name, voice_name=params.host.voice_name)
    guest1 = GuestAgent(name=params.guests[0].name, company=params.guests[0].company,
                        characteristics=params.guests[0].characteristics, voice_name=params.guests[0].voice_name)
    guest2 = GuestAgent(name=params.guests[1].name, company=params.guests[1].company,
                        characteristics=params.guests[1].characteristics, voice_name=params.guests[1].voice_name)

    podcast = PodcastAgent(topic=params.host.topic,
                           host=host, guests=[guest1, guest2])
    history = podcast.run()
    return history

# async def synthesize_speech(text, voice_name="nova", filename="output.mp3"):
#     url = "https://api.openai.com/v1/audio/speech"
#     headers = {
#         "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "tts-1",              # or "tts-1-hd"
#         "input": text,
#         "voice": voice_name,
#         "response_format": "mp3"
#     }
#     response = requests.post(url, headers=headers, json=data)
#     if response.ok:
#         with open(filename, "wb") as f:
#             f.write(response.content)
#         print(f"Saved to {filename}")
#     else:
#         print("Error:", response.text)


async def synthesize_speech(text, voice_name="nova"):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "tts-1",
        "input": text,
        "voice": voice_name,
        "response_format": "mp3"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        return io.BytesIO(response.content)
    else:
        raise Exception(
            f"TTS API error: {response.status_code} {response.text}")
