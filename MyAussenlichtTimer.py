import requests, time, datetime
from enum import Enum
from suntime import Sun, SunTimeException

class AussenlichtState(Enum):
    OFF = 0
    ON = 1
    NO_ACTION = 2

class AussenlichtConfig():
    AUSSENLICHT_URL = "http://192.168.178.78"
    LATITUDE = 50.0212981
    LONGITUDE = 9.2554408


def is_server_available():
    url = AussenlichtConfig.AUSSENLICHT_URL
    response = requests.get(url)
    if response.status_code == 200:
        print("Connection to {s} successful!".format(s=url))
        return True
    else:
        return False


def turn_light_on(verbose=False):
    url = AussenlichtConfig.AUSSENLICHT_URL
    requests.post(url + "/?ON")
    if verbose is True:
        print("Außenlicht ON")


def turn_light_off(verbose=False):
    url = AussenlichtConfig.AUSSENLICHT_URL
    requests.post(url + "/?OFF")
    if verbose is True:
        print("Außenlicht OFF")


def get_sunrise_and_sunset(today=None):
    sun = Sun(lat=AussenlichtConfig.LATITUDE, lon=AussenlichtConfig.LONGITUDE)
    if today == None:
        today_sunrise = sun.get_local_sunrise_time()
        today_sunset = sun.get_local_sunset_time()
    else:
        today_sunrise = sun.get_local_sunrise_time(today)
        today_sunset = sun.get_local_sunset_time(today)

    return [today_sunrise, today_sunset]


def toggle_aussenlicht_with_sun(
    tzinfo, iterations=60 * 3, delay_in_secs=1, verbose=True, now=None
):
    for i in range(iterations):
        state = AussenlichtState.NO_ACTION

        if now == None:
            now = datetime.datetime.now(tzinfo)

        sun_rise_and_set_list = get_sunrise_and_sunset(now)
        sunrise_time = sun_rise_and_set_list[0]
        sunset_time = sun_rise_and_set_list[1]

        midnight = sunset_time.replace(hour=23, minute=59)
        last_midnight = sunrise_time.replace(hour=0, minute=1)

        print(
            "now: {n}\t last_midnight: {lm}\t midnight: {m}\t sunrise: {sr}\t sunset: {ss}\t".format(
                n=now, lm=last_midnight, m=midnight, sr=sunrise_time, ss=sunset_time
            )
        )

        if last_midnight < now < sunset_time:
            turn_light_off(verbose)
            state = AussenlichtState.OFF
        elif sunset_time < now < midnight:
            turn_light_on(verbose)
            state = AussenlichtState.ON
        else:
            print("No Action")

        time.sleep(delay_in_secs)
        return state


if __name__ == "__main__":
    print("Fetching sunrise and sunset times...")
    sun_rise_and_set_list = get_sunrise_and_sunset()
    print(sun_rise_and_set_list)
    sunrise_time = sun_rise_and_set_list[0]
    sunset_time = sun_rise_and_set_list[1]
    tzinfo = sunrise_time.tzinfo

    print("Testing Conncetion to Server...")
    if is_server_available() is True:
        toggle_aussenlicht_with_sun(tzinfo=tzinfo)
