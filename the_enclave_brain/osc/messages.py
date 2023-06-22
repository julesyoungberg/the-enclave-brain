from pythonosc.udp_client import SimpleUDPClient

osc_client = SimpleUDPClient("127.0.0.1", 8010)


def send_osc_message(address: str, value: float, debug=False):
    if debug:
        print(f"sending message: address={address}, value={value}")
    osc_client.send_message(address, [value])
