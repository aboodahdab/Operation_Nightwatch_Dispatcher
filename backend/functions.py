import struct
import json
from pathlib import Path
import os
import uuid
import time
from redis_usage import dump_data_into_redis
PATH = "data.json"
HISTORY_FILE_PATH = "coords_History.json"


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


def add_to_data(path, query):
    if path == HISTORY_FILE_PATH:
        tmp = f"{path}.{uuid.uuid4().hex}"
        with open(tmp, "w") as f:
            json.dump(query, f, indent=2)
        os.replace(tmp, path)  # atomic swap, no partial-write window
        return

    with open(path, "w") as file:
        json.dump(query, file)


def create_file(path):
    with open(path, "w"):
        pass


def read_file(path):
    if not os.path.exists(path):
        create_file(path)
    content = Path(path).read_text()
    if not content:
        add_to_data(path, {})
        return {}
    with open(path, "r") as file:
        data = json.load(file)
        return data


def clear_terminal():

    print("\033[H\033[J")
    print("FLEET STATUS — 10 vehicles")
    print("=====" * 20)


def print_result(data):

    clear_terminal()
    for i in data.items():
        index = int(i[0])
        specs = i[1]
        specs_len = len(specs)

        name = get_name(index)

        if specs_len == 3:
            speed = specs["SPEED"]
            fuel = specs["FUEL"]
            gps = specs["GPS"]
            lat = gps[0]
            lon = gps[1]
            print(
                f"{name:<15} SPEED {speed:>6} km/h   FUEL {fuel:>4}%   POS {lat:>9}, {lon:>9}")


def history_handler(vehicle_type, arr):
    # every 4 hours = 14400
    dump_data_into_redis("history", {vehicle_type: json.dumps(arr)})
    return


def add_to_data_handler(vehicle_type, packet_type, packet):
    # start time is 4.6 for example:
    file_contents = read_file(PATH)
    vehicle_type = str(vehicle_type)

    this_one = None
    dictionary = {}
    if vehicle_type not in file_contents:
        file_contents[vehicle_type] = {}
        this_one = file_contents[vehicle_type]

    else:
        this_one = file_contents[vehicle_type]

    if packet_type == 1:
        # speed packet
        speed = packet
        dictionary = {vehicle_type: json.dumps({"SPEED": packet})}

        this_one["SPEED"] = speed

    if packet_type == 2:
        # gps packet
        lat = packet[0]
        lon = packet[1]
        arr = [lat, lon]

        history_handler(vehicle_type, arr, )
        dictionary = {vehicle_type: json.dumps({"GPS": arr})}
        this_one["GPS"] = arr

    if packet_type == 3:
        # fuel packet
        fuel = packet
        this_one["FUEL"] = fuel
        dictionary = {vehicle_type: json.dumps({"FUEL": packet})}

    add_to_data(PATH, file_contents)

    print_result(file_contents)
    dump_data_into_redis("data", dictionary)
