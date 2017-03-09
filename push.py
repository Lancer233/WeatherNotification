from pushbullet import Pushbullet
import requests
import json

def main():
    r = requests.get('http://api.caiyunapp.com/v2/TAkhjf8d1nlSlspN/121.483,31.2333/forecast')
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
    if abs(diff_avg_temp) > 2 or abs(diff_max_temp) > 2 or abs(diff_min_temp) >2:
        output_string = "Warning!!! "
    tomorrow_avg_rain = json_data["result"]["daily"]["precipitation"][0]["avg"];
    if tomorrow_avg_rain >= 0.15:
        output_string += "Heavy Raining "
    elif tomorrow_avg_rain >= 0.05:
        output_string += "Raining "
    
    output_string += "tomorrow temperature is " + str(tomorrow_min_temp) +  " "+str(tomorrow_avg_temp) + " "+str(tomorrow_max_temp)
    
    output_string += " send from HG's server"

    pb = Pushbullet("o.9lJnDiHR3BZGUh0aV33Jc8NqvTn5W0nX")

    push = pb.push_note(output_string, output_string)

if __name__ == "__main__":
    main()
