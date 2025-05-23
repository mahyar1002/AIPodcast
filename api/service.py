from agents.host_agent import HostAgent
from agents.guest_agent import GuestAgent
from agents.podcast_agent import PodcastAgent
from .schema import InitiateRequest


async def initiate_agents(params: InitiateRequest):
    host = HostAgent(name=params.host.name)
    guest1 = GuestAgent(name=params.guests[0].name, company=params.guests[0].comapny,
                        characteristics=params.guests[0].characteristics)
    guest2 = GuestAgent(name=params.guests[1].name, company=params.guests[1].comapny,
                        characteristics=params.guests[1].characteristics)

    podcast = PodcastAgent(topic=params.host.topic,
                           host=host, guests=[guest1, guest2])
    history = podcast.run()
    return history