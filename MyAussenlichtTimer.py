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

    def get_timezone_info(self):
        tzinfo = self.sunrise.tzinfo
        return tzinfo


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


class Evaluate:
    def __init__(self, TimeCache, now):
        self.TimeObject = TimeCache
        self.now = now

    def compute_aussenlicht_state(self):
        state = AussenlichtState.NO_ACTION
        to = self.TimeObject
        now = self.now
        if to.last_midnight < now < to.sunset:
            state = AussenlichtState.OFF
        elif to.sunset < now < to.midnight:
            state = AussenlichtState.ON
        else:
            print("No Action")
        return state


class Output:
    @staticmethod
    def print_times(TimeObject, now):
        t = TimeObject
        print(
            "now: {n}\t last_midnight: {lm}\t midnight: {m}\t sunrise: {sr}\t \
                sunset: {ss}\t".format(
                n=now, lm=t.last_midnight, m=t.midnight, sr=t.sunrise, ss=t.sunset
            )
        )


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
    Network = Networking(AussenlichtConfig)
    for i in range(iterations):
        state = AussenlichtState.NO_ACTION

        if now is None:
            now = datetime.datetime.now(tzinfo)

        TodaysTimeEvents = set_time_events_for_today(now)
        Output.print_times(TodaysTimeEvents, now)
        EvaluateTimes = Evaluate(TodaysTimeEvents, now)
        state_to_set = EvaluateTimes.compute_aussenlicht_state()

        if state_to_set == AussenlichtState.OFF:
            Network.turn_light_off(verbose)
        elif state_to_set == AussenlichtState.ON:
            Network.turn_light_on(verbose)
        else:
            pass

        time.sleep(delay_in_secs)
        return state_to_set


if __name__ == "__main__":
    print("Fetching sunrise and sunset times...")
    TodaysTimeEvents = set_time_events_for_today()
    tzinfo = TodaysTimeEvents.get_timezone_info()
    now = datetime.datetime.now(tzinfo)
    Output.print_times(TodaysTimeEvents, now)

    print("Testing Conncetion to Server...")
    if Networking.is_server_available() is True:
        toggle_aussenlicht_with_sun(tzinfo=tzinfo)
