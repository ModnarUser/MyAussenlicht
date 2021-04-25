from Source.Networking import Networking
import datetime
import csv
import pytest
import httpretty

################################################################
# Test Settings
################################################################
class TestConfig:
    AUSSENLICHT_URL = "http://192.168.178.78"
    LATITUDE = 50.0212981
    LONGITUDE = 9.2554408

@httpretty.activate
def test_is_server_available():
    httpretty.enable()
    httpretty.register_uri(
        httpretty.GET, TestConfig.AUSSENLICHT_URL, status=200
    )
    Network = Networking(TestConfig)
    assert Network.is_server_available() is True
    httpretty.disable()


@httpretty.activate
def test_turn_light_on():
    Network = Networking(TestConfig)
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, Network.url + "/?ON")

    Network.turn_light_on(verbose=False)
    req = httpretty.last_request()
    assert req.method == "POST"
    url = "http://" + req.headers.get("Host", "") + req.path
    assert url == Network.url + "/?ON"
    httpretty.disable()


@httpretty.activate
def test_turn_light_off():
    Network = Networking(TestConfig)
    httpretty.enable()
    httpretty.register_uri(httpretty.POST, Network.url + "/?OFF")

    Network.turn_light_off(verbose=False)
    req = httpretty.last_request()
    assert req.method == "POST"
    url = "http://" + req.headers.get("Host", "") + req.path
    assert url == Network.url + "/?OFF"
    httpretty.disable()