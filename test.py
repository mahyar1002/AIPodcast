
from agents.host_agent import HostAgent
from agents.guest_agent import GuestAgent
from agents.podcast_agent import PodcastAgent

host = HostAgent(name="Samuel")
guest1 = GuestAgent(name="Anna", company="Telenor", characteristics="Friendly, data-driven, loyal to Telenor.")
guest2 = GuestAgent(name="Bjorn", company="Telia", characteristics="Confident, persuasive, passionate about Telia.")

podcast = PodcastAgent(topic="Which telecom company is better?", host=host, guests=[guest1, guest2])
history = podcast.run()

# Print or return the full transcript
for line in history:
    print(f"{line['role']}: {line['message']}")