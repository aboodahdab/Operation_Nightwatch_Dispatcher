import struct
import json

FILENAME = "data.json"


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


def print_result(full):
    for i in full.items():
        index = int(i[0])
        name = get_name(index).strip()
        elements = i[1]

        speed = None

        fuel = None
        gps = None
        lat = gps[0]
        lon = gps[1]
        print(
            f"{name:<18} SPEED {speed:>6} km/h   FUEL {fuel:>4}%   POS {lat:>9}, {lon:>9}")


def add_to_data(query):

    with open(FILENAME, "w") as file:
        json.dump(query, file)


def add_to_data_handler(vehicle_type, packet_type, packet):

    file_contents = None

    vehicle_type = str(vehicle_type)

    with open(FILENAME, "r") as file:
        file_contents = json.load(file)

    this_one = None
    if vehicle_type not in file_contents:
        file_contents[vehicle_type] = {}
        this_one = file_contents[vehicle_type]

    else:
        this_one = file_contents[vehicle_type]

    if packet_type == 1:
        # speed packet
        speed = packet

        this_one["SPEED"] = speed
        print("SPEED", this_one)

    if packet_type == 2:
        # speed packet
        lat = packet[0]
        lon = packet[1]

        arr = [lat, lon]

        this_one["GPS"] = arr

    if packet_type == 3:
        # speed packet
        fuel = packet
        this_one["FUEL"] = fuel

    add_to_data(file_contents)
    # print_result(file_contents)
