import time
import datetime
from suntime import Sun
from Stdout import Printer
import TimeEvents as te
from Networking import Networking
from Config import AussenlichtConfig


if __name__ == "__main__":
    print("Fetching sunrise and sunset times...")
    TodaysTimeEvents = te.set_time_events_for_today()
    tzinfo = TodaysTimeEvents.get_timezone_info()
    now = datetime.datetime.now(tzinfo)
    Printer.print_times(TodaysTimeEvents, now)

    print("Testing Conncetion to Server...")
    if Networking(AussenlichtConfig).is_server_available() is True:
        te.toggle_aussenlicht_with_sun(tzinfo=tzinfo)
