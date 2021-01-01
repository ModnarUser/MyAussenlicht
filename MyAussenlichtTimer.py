import requests, time, datetime
from suntime import Sun, SunTimeException

AUSSENLICHT_URL = "http://192.168.178.78"
LATITUDE = 50.0212981
LONGITUDE = 9.2554408

def is_server_available():
    response = requests.get(AUSSENLICHT_URL)
    if response.status_code is 200:
        print("Connection to {s} successful!".format(s=AUSSENLICHT_URL))
        return True
    else:
        return False

def turn_light_on(verbose):
    requests.post("http://192.168.178.78/?ON")
    if verbose is True:
        print("Außenlicht ON")

def turn_light_off(verbose):
    requests.post("http://192.168.178.78/?OFF")
    if verbose is True:
        print("Außenlicht OFF")

def get_sunrise_and_sunset():
    sun = Sun(lat=LATITUDE, lon=LONGITUDE)
    today_sunrise = sun.get_local_sunrise_time()
    today_sunset = sun.get_local_sunset_time()
    return [today_sunrise, today_sunset]

def main():
    print("Fetching sunrise and sunset times...")
    sun_rise_and_set_list = get_sunrise_and_sunset()
    print(sun_rise_and_set_list)
    sunrise_time = sun_rise_and_set_list[0]
    sunset_time = sun_rise_and_set_list[1]
    
    print("Testing Conncetion to Sever...")
    if (is_server_available() is True):
        while True:
            now = datetime.datetime.now(sunrise_time.tzinfo)        
            midnight = sunset_time.replace(hour=23, minute=59)
            last_midnight = midnight.replace(hour=0, minute=0)
            
            print("\nCurrent Time is:", now)
            print("Sunset Today: ", sunset_time)
            print("Sunrise Today: ", sunrise_time)
            #print(midnight)
            #print(last_midnight)

            if last_midnight < now < sunset_time:
                turn_light_off(verbose=False)
            elif sunset_time < now < midnight:
                turn_light_on(verbose=False)
            else:
                print("No Action")
            
            time.sleep(60*5)
            
            print("Fetching sunrise and sunset times...")
            sun_rise_and_set_list = get_sunrise_and_sunset()
            print(sun_rise_and_set_list)
            sunrise_time = sun_rise_and_set_list[0]
            sunset_time = sun_rise_and_set_list[1]
main()