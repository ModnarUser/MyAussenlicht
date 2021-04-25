import requests

class Networking:
    def __init__(self, AussenlichtConfig):
        self.url = AussenlichtConfig.AUSSENLICHT_URL

    def is_server_available(self):
        url = self.url
        response = requests.get(url)
        if response.status_code == 200:
            print("Connection to {s} successful!".format(s=url))
            return True
        else:
            return False

    def turn_light_on(self, verbose=False):
        url = self.url
        requests.post(url + "/?ON")
        if verbose is True:
            print("Außenlicht ON")

    def turn_light_off(self, verbose=False):
        url = self.url
        requests.post(url + "/?OFF")
        if verbose is True:
            print("Außenlicht OFF")
