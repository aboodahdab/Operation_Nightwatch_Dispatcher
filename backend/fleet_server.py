#!/usr/bin/env python3
"""
fleet_server.py  —  Binary UDP telemetry sender (10 moving vehicles).
DO NOT MODIFY THIS FILE AND TREAT IT LIKE A BLACK BOX
Usage:
    python3 fleet_server.py                  # broadcast on the LAN, port 50505
    python3 fleet_server.py --host 127.0.0.1 # loopback only (solo testing)
    python3 fleet_server.py --host <his-ip>  # unicast to a specific machine
    python3 fleet_server.py --rate 5         # ~5 update cycles/sec
Stop with Ctrl-C.
"""

import argparse
import math
import random
import socket
import struct
import time

PORT = 50505

# ---------------------------------------------------------------------------
# PACKET FORMAT  (this is the contract documented in TASK.md)
#
# 2-byte header, big-endian:
#     byte 0 : message type   (1 = SPEED, 2 = GPS, 3 = FUEL)
#     byte 1 : vehicle id      (0-9, maps to a name -- see FLEET below)
#
# Body depends on the type:
#     SPEED (type 1):  1 float  -> speed in km/h            ">f"   (4 bytes)
#     GPS   (type 2):  2 floats -> latitude, longitude      ">ff"  (8 bytes)
#     FUEL  (type 3):  1 uint    -> fuel percent 0-100       ">I"   (4 bytes)
SPEED_FMT = ">BBf"    # type, id, speed
GPS_FMT   = ">BBff"   # type, id, lat, lon
FUEL_FMT  = ">BBI"    # type, id, fuel_percent

TYPE_SPEED, TYPE_GPS, TYPE_FUEL = 1, 2, 3

# Coordinates are folded into these symmetric ranges, so a vehicle that walks
# off one edge reappears on the opposite one (lat +90 -> -90, lon +180 -> -180).
LAT_LIMIT = 90.0
LON_LIMIT = 180.0

# id -> (name, kind, start_lat, start_lon, cruising_kmh, step)
#   kind is just flavor. 'step' scales how far it moves per cycle
#   (planes move faster / farther than ground vehicles).
FLEET = {
    0: ("Rusty Rocket",     "van",   41.33,  19.82,  70,  0.010),
    1: ("Silver Arrow",     "car",   45.46,   9.19, 115,  0.014),
    2: ("Sky Whale",        "plane", 48.85,   2.35, 780,  0.090),
    3: ("Midnight Courier", "van",   52.52,  13.40,  65,  0.010),
    4: ("Thunderbird",      "plane", 51.51,  -0.13, 820,  0.095),
    5: ("Green Machine",    "car",   40.42,  -3.70, 125,  0.015),
    6: ("Iron Pigeon",      "plane", 55.75,  37.62, 760,  0.088),
    7: ("Sandstorm",        "van",   30.04,  31.24,  75,  0.011),
    8: ("Blue Comet",       "car",   35.68, 139.65, 130,  0.016),
    9: ("Night Owl",        "plane", 40.71, -74.01, 800,  0.092),
}
# ---------------------------------------------------------------------------


def wrap(value, limit):
    """Fold value into [-limit, limit); +limit comes out as -limit."""
    span = 2 * limit
    return (value + limit) % span - limit


class Vehicle:
    def __init__(self, vid, name, kind, lat, lon, cruise, step):
        self.vid = vid
        self.name = name
        self.kind = kind
        self.home = (lat, lon)
        self.lat = lat
        self.lon = lon
        self.cruise = cruise
        self.step = step
        self.heading = random.uniform(0, 2 * math.pi)
        self.fuel = 100

    def update(self):
        # wander: nudge heading a little each cycle for an organic path
        self.heading += random.uniform(-0.3, 0.3)

        # roam freely; walking off an edge reappears on the opposite one
        self.lat = wrap(self.lat + math.cos(self.heading) * self.step, LAT_LIMIT)
        self.lon = wrap(self.lon + math.sin(self.heading) * self.step, LON_LIMIT)

        # fuel slowly burns; refuel when low
        self.fuel -= random.uniform(0.2, 0.6)
        if self.fuel < 12:
            self.fuel = 100
        return max(0, int(self.fuel))

    def speed(self):
        return self.cruise + random.uniform(-8, 8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="255.255.255.255",
                    help="destination address (default: LAN broadcast). "
                         "Use 127.0.0.1 to test on one machine, or an IP to "
                         "send to a specific machine.")
    ap.add_argument("--port", type=int, default=PORT)
    ap.add_argument("--rate", type=float, default=2.0,
                    help="update cycles per second (default 2)")
    args = ap.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    fleet = [Vehicle(vid, *rest) for vid, rest in FLEET.items()]
    interval = 1.0 / args.rate

    print(f"Dispatching {len(fleet)} vehicles to {args.host}:{args.port} "
          f"at ~{args.rate} cycles/s. Ctrl-C to stop.")

    try:
        while True:
            for v in fleet:
                fuel = v.update()
                sock.sendto(struct.pack(SPEED_FMT, TYPE_SPEED, v.vid, v.speed()),
                            (args.host, args.port))
                sock.sendto(struct.pack(GPS_FMT, TYPE_GPS, v.vid, v.lat, v.lon),
                            (args.host, args.port))
                sock.sendto(struct.pack(FUEL_FMT, TYPE_FUEL, v.vid, fuel),
                            (args.host, args.port))
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
