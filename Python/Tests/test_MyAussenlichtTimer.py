from Source import MyAussenlichtTimer as Al
from Source import Networking as Net
from Net import Networking 
import datetime
import csv
import pytest
import httpretty

################################################################
# Test Settings
################################################################

TEST_URL = "http://192.168.178.78"  # Use URL of your Aussenlicht
Al.AussenlichtConfig.AUSSENLICHT_URL = TEST_URL

Today = datetime.datetime(
    2021, 3, 31, 0, 0, 0, 597403, tzinfo=datetime.timezone(datetime.timedelta(hours=2))
)
TEST_TZINFO = datetime.timezone(datetime.timedelta(hours=2))

################################################################
# Helper Functions
################################################################


def generate_list_of_datetimes():
    date_list = []

    date_list_1 = [Today + datetime.timedelta(minutes=x) for x in range(0, 24 * 60)]
    date_list_2 = [
        Today + datetime.timedelta(days=1, minutes=x) for x in range(0, 24 * 60)
    ]
    date_list_3 = [
        Today + datetime.timedelta(days=2, minutes=x) for x in range(0, 24 * 60)
    ]

    date_list = date_list_1 + date_list_2 + date_list_3
    return date_list


################################################################
# Test Cases
################################################################





@pytest.mark.parametrize(
    "test_time, aussenlicht_state",
    [
        (
            datetime.datetime(2021, 3, 31, 0, 0, 0, 597403, tzinfo=TEST_TZINFO),
            Al.AussenlichtState.NO_ACTION,
        ),
        (
            datetime.datetime(2021, 6, 15, 13, 0, 0, 597403, tzinfo=TEST_TZINFO),
            Al.AussenlichtState.OFF,
        ),
        (
            datetime.datetime(2021, 12, 1, 21, 0, 0, 597403, tzinfo=TEST_TZINFO),
            Al.AussenlichtState.ON,
        ),
    ],
)
@httpretty.activate
def test_specific_datetimes(test_time, aussenlicht_state):
    Network = Networking(Al.AussenlichtConfig)
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, Network.url, status=200)

    httpretty.register_uri(httpretty.POST, Network.url + "/?OFF")
    httpretty.register_uri(httpretty.POST, Network.url + "/?ON")
    state = Al.toggle_aussenlicht_with_sun(
        tzinfo=TEST_TZINFO,
        iterations=1,
        delay_in_secs=0.0001,
        verbose=False,
        now=test_time,
    )
    httpretty.disable()
    assert state == aussenlicht_state


@httpretty.activate
def test_simulate_for_number_of_days():
    Network = Networking(Al.AussenlichtConfig)
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, Network.url, status=200)

    httpretty.register_uri(httpretty.POST, Network.url + "/?OFF")
    httpretty.register_uri(httpretty.POST, Network.url + "/?ON")

    tzinfo = datetime.timezone(datetime.timedelta(hours=2))

    states = []
    date_list = generate_list_of_datetimes()
    for i in range(len(date_list)):
        state = Al.toggle_aussenlicht_with_sun(
            tzinfo=tzinfo,
            iterations=1,
            delay_in_secs=0.0001,
            verbose=False,
            now=date_list[i].replace(tzinfo=tzinfo),
        )
        states.append([date_list[i], int(state.value)])

    file = open("./test_MyAussenlicht.csv", "w+", newline="")

    with file:
        write = csv.writer(file)
        write.writerows(states)

    a = open("./Ressources/valid_log.csv", "r").read()
    b = open("./test_MyAussenlicht.csv", "r").read()

    assert a == b
    httpretty.disable()
