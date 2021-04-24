import requests
import time
import datetime
from enum import Enum
from suntime import Sun


class AussenlichtState(Enum):
    OFF = 0
    ON = 1
    NO_ACTION = 2


class AussenlichtConfig:
    AUSSENLICHT_URL = "http://192.168.178.78"
    LATITUDE = 50.0212981
    LONGITUDE = 9.2554408


class TimeCache:
    def __init__(self, sunrise, sunset, midnight, last_midnight):
        self.sunrise = sunrise
        self.sunset = sunset
        self.midnight = midnight
        self.last_midnight = last_midnight


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


def set_time_events_for_today(today=None):
    sun = Sun(lat=AussenlichtConfig.LATITUDE, lon=AussenlichtConfig.LONGITUDE)
    if today is None:
        today_sunrise = sun.get_local_sunrise_time()
        today_sunset = sun.get_local_sunset_time()
    else:
        today_sunrise = sun.get_local_sunrise_time(today)
        today_sunset = sun.get_local_sunset_time(today)

    TodaysTimes = TimeCache(
        sunrise=today_sunrise,
        sunset=today_sunset,
        midnight=today_sunset.replace(hour=23, minute=59),
        last_midnight=today_sunrise.replace(hour=0, minute=1),
    )
    return TodaysTimes


def toggle_aussenlicht_with_sun(
    tzinfo, iterations=60 * 3, delay_in_secs=1, verbose=True, now=None
):
    for i in range(iterations):
        state = AussenlichtState.NO_ACTION

        if now is None:
            now = datetime.datetime.now(tzinfo)

        TodaysTimeEvents = set_time_events_for_today(now)
        sunrise_time = TodaysTimeEvents.sunrise
        sunset_time = TodaysTimeEvents.sunset
        midnight = TodaysTimeEvents.midnight
        last_midnight = TodaysTimeEvents.last_midnight

        print(
            "now: {n}\t last_midnight: {lm}\t midnight: {m}\t sunrise: {sr}\t \
                sunset: {ss}\t".format(
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
    TodaysTimeEvents = set_time_events_for_today()
    sunrise_time = TodaysTimeEvents.sunrise
    sunset_time = TodaysTimeEvents.sunset
    print("sunrise: {rise}\nsunset: {set}\n".format(rise=sunrise_time, set=sunset_time))
    tzinfo = sunrise_time.tzinfo

    print("Testing Conncetion to Server...")
    if is_server_available() is True:
        toggle_aussenlicht_with_sun(tzinfo=tzinfo)
