import struct
import json
from pathlib import Path
import time
import os
from redis_usage import dump_data_into_redis
PATH = "data.json"
CLEANING_TIME=0.5

def get_gps(data):

    parsed_data_gps = struct.unpack(">BBff", data)

    return parsed_data_gps


def get_speed(data):
    parsed_data_speed = struct.unpack(">BBf", data)
    return parsed_data_speed


def get_fuel(data):
    parsed_data_fuel = struct.unpack(">BBI", data)
    return parsed_data_fuel


def get_name(index):
    names_array = ["Rusty Rocket",
                   "Silver Arrow",
                   "Sky Whale",
                   "Midnight Courier",
                   "Thunderbird",
                   "Green Machine",
                   "Iron Pigeon",
                   "Sandstorm",
                   "Blue Comet",
                   "Night Owl", ]
    return names_array[index]


def add_to_data(query):

    with open(PATH, "w") as file:
        json.dump(query, file)

def create_file():
  with open(PATH,"w"):
     pass
def read_file():
    if not os.path.exists(PATH):
       create_file()
    content = Path(PATH).read_text()
    if not content:
         add_to_data({})
         return {}
    with open(PATH, "r") as file:
            data = json.load(file)
            return data


def clear_terminal():
    
    time.sleep(CLEANING_TIME)
    print("\033[H\033[J")
    print(f"Terminal cleaned ({CLEANING_TIME}s)")

def print_result(data):

    for i in data.items():
        index = int(i[0])
        specs = i[1]
        specs_len = len(specs)
        name=get_name(index)

        if specs_len==3:
           speed= specs["SPEED"]
           fuel=specs["FUEL"]
           gps=specs["GPS"]
           lat=gps[0]
           lon=gps[1]
           clear_terminal()
           print(f"{name:<15} SPEED {speed:>6} km/h   FUEL {fuel:>4}%   POS {lat:>9}, {lon:>9}")

 
def add_to_data_handler(vehicle_type, packet_type, packet):

    file_contents = read_file()
    print(packet,"packet")
    vehicle_type = str(vehicle_type)
   
    this_one = None
    dictionary={}
    if vehicle_type not in file_contents:
        file_contents[vehicle_type] = {}
        this_one = file_contents[vehicle_type]

    else:
        this_one = file_contents[vehicle_type]

    if packet_type == 1:
        # speed packet
        speed = packet
        dictionary={vehicle_type:json.dumps({"SPEED":packet})}


        this_one["SPEED"] = speed


    if packet_type == 2:
        # gps packet
        lat = packet[0]
        lon = packet[1]

        arr = [lat, lon]
        dictionary={vehicle_type:json.dumps({"GPS":arr})}


        this_one["GPS"] = arr

    if packet_type == 3:
        # fuel packet
        fuel = packet
        this_one["FUEL"] = fuel
        dictionary={vehicle_type:json.dumps({"FUEL":packet})}

    add_to_data(file_contents)
    print(dictionary)
    print_result(file_contents)
    dump_data_into_redis(dictionary)



