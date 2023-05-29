from pythonosc.udp_client import SimpleUDPClient

osc_client = SimpleUDPClient("127.0.0.1", 8010)


def send_osc_message(address: str, value: float):
    osc_client.send_message(address, [value])
