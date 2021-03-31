import MyAussenlichtTimer as Al
import datetime
from enum import Enum 
import csv
import pytest
import filecmp

Al.AUSSENLICHT_URL = "http://192.168.178.78" # Use URL of your Aussenlicht

Today = datetime.datetime(2021, 3, 31, 0, 0, 0, 597403)
date_list_1 = [Today + datetime.timedelta(minutes=x) for x in range(0, 24*60)]
date_list_2 = [Today + datetime.timedelta(days=1, minutes=x) for x in range(0, 24*60)]
date_list_3 = [Today + datetime.timedelta(days=2, minutes=x) for x in range(0, 24*60)]

date_list = date_list_1 + date_list_2 + date_list_3

def test_toggle_aussenlicht():
    sun_rise_and_set_list = Al.get_sunrise_and_sunset()
    print(sun_rise_and_set_list)
    sunrise_time = sun_rise_and_set_list[0]
    sunset_time = sun_rise_and_set_list[1]
    tzinfo=sunrise_time.tzinfo

    states = []

    for i in range(len(date_list)):
        state = Al.toggle_aussenlicht_with_sun(tzinfo=tzinfo, iterations=1, delay_in_secs=0.0001, verbose=False, now=date_list[i].replace(tzinfo=sunrise_time.tzinfo))
        states.append([date_list[i].replace(tzinfo=sunrise_time.tzinfo), int(state.value)])

    # opening the csv file in 'w+' mode
    file = open('test_MyAussenlicht.csv', 'w+', newline ='')
    
    print(states)
    # writing the data into the file
    with file:    
        write = csv.writer(file)
        write.writerows(states)

    result = filecmp.cmp('Ressources/valid_log.csv', 'test_MyAussenlicht.csv')
    assert result == True
