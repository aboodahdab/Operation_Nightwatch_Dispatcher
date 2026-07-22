import socket
from functions import get_speed, get_fuel, get_gps, get_name, add_to_data_handler
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 50505))
print("FLEET STATUS — 10 vehicles")
print("-----"*30)


def handler(first_2, data):
    if first_2 == "01":
        parsed_data_speed = get_speed(data)
        packet_type = int(parsed_data_speed[0])
        vehicle_type = int(parsed_data_speed[1])
        speed = round(parsed_data_speed[2])
        name = get_name(vehicle_type)
        add_to_data_handler(vehicle_type, packet_type, (speed))

    elif first_2 == "02":
        parsed_data_gps = get_gps(data)
        packet_type = int(parsed_data_gps[0])
        vehicle_type = int(parsed_data_gps[1])
        latitude = parsed_data_gps[2]
        longitiude = parsed_data_gps[3]
        name = get_name(vehicle_type)

        print(type(vehicle_type), "type yoooooo")
        add_to_data_handler(vehicle_type, packet_type, (latitude, longitiude))

    elif first_2 == "03":
        parsed_data_fuel = get_fuel(data)
        packet_type = int(parsed_data_fuel[0])
        vehicle_type = int(parsed_data_fuel[1])
        fuel_percent = parsed_data_fuel[2]
        name = get_name(vehicle_type)
        add_to_data_handler(vehicle_type, packet_type, (fuel_percent))
        print(vehicle_type, fuel_percent, "FUEL")
    # print("\033[H\033[J")


for i in range(300):

    data, addr = server_socket.recvfrom(1024)  # receive up to 1024 bytes

    value = data.hex()
    first_2 = value[:2]
    handler(first_2, data)
