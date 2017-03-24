from pushbullet import Pushbullet
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import requests
import json


def get_weather_and_push():
    token_pb = open('pb_token').readline().strip()
    token_weather = open('weather_token').readline().strip()

    r = requests.get('http://api.caiyunapp.com/v2/'+token_weather+'/121.483,31.2333/forecast')
    json_data = json.loads(r.text)
    today_min_temp = json_data["result"]["daily"]["temperature"][0]['min']
    today_max_temp = json_data["result"]["daily"]["temperature"][0]['max']
    today_avg_temp = json_data["result"]["daily"]["temperature"][0]['avg']
    tomorrow_min_temp = json_data["result"]["daily"]["temperature"][1]['min']
    tomorrow_max_temp = json_data["result"]["daily"]["temperature"][1]['max']
    tomorrow_avg_temp = json_data["result"]["daily"]["temperature"][1]['avg']
    diff_min_temp = tomorrow_min_temp - today_min_temp
    diff_max_temp = tomorrow_max_temp - today_max_temp
    diff_avg_temp = tomorrow_avg_temp - today_avg_temp
    output_string = ""
    if abs(diff_avg_temp) > 2 or abs(diff_max_temp) > 2 or abs(diff_min_temp) >2:
        output_string = "Warning!!! "
    if diff_avg_temp > 2:
        output_string += "temperature higher "
    else:
        output_string += "temperature lower "

    tomorrow_avg_rain = json_data["result"]["daily"]["precipitation"][0]["avg"];
    if tomorrow_avg_rain >= 0.15:
        output_string += "Heavy Raining "
    elif tomorrow_avg_rain >= 0.05:
        output_string += "Raining "
    
    output_string += "Today temperature is " + str(today_min_temp) +  " "+str(today_avg_temp) + " "+str(today_max_temp)+" "
    output_string += "Tomorrow temperature is " + str(tomorrow_min_temp) +  " "+str(tomorrow_avg_temp) + " "+str(tomorrow_max_temp)+" "
    output_string += "Precipitation is " + str(tomorrow_avg_rain)
    output_string += " Send from HG's server"
    pb = Pushbullet(token)

    push = pb.push_note(output_string, output_string)

def my_timer():
    scheduler = BlockingScheduler()
    scheduler.add_job(get_weather_and_push, 'cron', day_of_week='1-7', hour=13, minute=30)
    print("scheduler start")
    scheduler.start()

if __name__ == "__main__":
    # push at the program begin, as debug
    get_weather_and_push();    
    my_timer();

