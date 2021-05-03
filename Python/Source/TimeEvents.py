import time
import datetime
from suntime import Sun

# Pretty hacky way to make test work
try:
    from .Config import AussenlichtConfig
    from .Networking import Networking
    from .Stdout import Printer
    from .Computation import Evaluate
    from .Computation import AussenlichtState
except:
    from Config import AussenlichtConfig
    from Networking import Networking
    from Stdout import Printer
    from Computation import Evaluate
    from Computation import AussenlichtState

class TimeCache:
    def __init__(self, sunrise, sunset, midnight, last_midnight):
        self.sunrise = sunrise
        self.sunset = sunset
        self.midnight = midnight
        self.last_midnight = last_midnight

    def get_timezone_info(self):
        tzinfo = self.sunrise.tzinfo
        return tzinfo


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
        Printer.print_times(TodaysTimeEvents, now)
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
