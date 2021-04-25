import time
import datetime
from suntime import Sun
from Networking import Networking
from Stdout import Printer
import TimeEvents as te

class AussenlichtConfig:
    AUSSENLICHT_URL = "http://192.168.178.78"
    LATITUDE = 50.0212981
    LONGITUDE = 9.2554408


if __name__ == "__main__":
    print("Fetching sunrise and sunset times...")
    TodaysTimeEvents = te.set_time_events_for_today()
    tzinfo = TodaysTimeEvents.get_timezone_info()
    now = datetime.datetime.now(tzinfo)
    Printer.print_times(TodaysTimeEvents, now)

    print("Testing Conncetion to Server...")
    if Networking(AussenlichtConfig).is_server_available() is True:
        te.toggle_aussenlicht_with_sun(tzinfo=tzinfo)
