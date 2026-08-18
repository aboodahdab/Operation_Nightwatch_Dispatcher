# ✈️ Operation Nightwatch — Fleet Dispatch Board
 
## The story
 
It is 2 a.m. You are the new night dispatcher for **Nightwatch Logistics**.
 
Ten vehicles are moving out there: some delivery vans, some fast cars, and some
airplanes. Each one sends its data back to base over the network.
 
But there is a problem. The old dispatcher left and took the dashboard program
with them. All you have now is the raw signal: a stream of **bytes** coming in
over the network. No names. No labels. Just bytes.
 
Your job: **read the bytes and build a new dashboard.** Turn the bytes back into
speed, position, and fuel — and show the **name** of each vehicle.
 
You only build the **receiver** (the program that reads and shows the data). The
fleet program that sends the data is already written for you (`fleet_server.py`)
— you run it, but you do not open it or change it. Treat it as a sealed box. Your
program must match its format **exactly**. If it does not match, you will read
wrong numbers.
 
This is the main idea: the format is an **agreement**. Both sides must use the
same one, byte for byte.
 
---
 
## Running the fleet (the sender)
 
You have a file called `fleet_server.py`. This is the "fleet" — it pretends to be
the 10 vehicles and sends out their data as UDP packets. You run it in one
terminal, and your own program (the receiver) runs in another terminal on the
same computer.
 
You need **Python 3** installed. Nothing else — it uses only built-in modules.
 
**Start the fleet like this:**
 
```
python3 fleet_server.py --host 127.0.0.1
```
 
`127.0.0.1` means "this same computer" (also called *localhost*). So the packets
are sent to your own machine, where your receiver is listening. This is all you
need for the whole project.
 
You should see a line like:
 
```
Dispatching 10 vehicles to 127.0.0.1:50505 at ~2.0 cycles/s. Ctrl-C to stop.
```
 
That means it is running and sending. Leave this terminal open. Open a **second**
terminal for your own program.
 
**Good to know:**
- The packets go to **UDP port 50505**. Your receiver must listen on that port.
- Stop the fleet any time with **Ctrl-C**.
- Want more or fewer updates per second? Add `--rate`, for example
  `python3 fleet_server.py --host 127.0.0.1 --rate 5` for 5 cycles a second.
- Always use `--host 127.0.0.1`. (Without it, the script tries to broadcast to a
  whole network, which is not what you want here and can behave strangely on one
  machine.)
You do not need to read or change `fleet_server.py`. Treat it as a sealed box
that sends bytes. Your job is only to receive and understand those bytes.
 
---
 
## The packet format (your agreement)
 
Every packet has a **2-byte header**, then a **body**. All numbers are
**big-endian** (this is the `>` in Python's `struct`).
 
### Header (same in every packet)
 
| byte | meaning       | type              |
|------|---------------|-------------------|
| 0    | message type  | unsigned byte (B) |
| 1    | vehicle id    | unsigned byte (B) |
 
**Byte 1** is the vehicle id: a number from **0 to 9**. It tells you *which*
vehicle sent the packet. You use it to find the name (see the list below).
 
**Byte 0** is the message type. It tells you how to read the rest of the packet:
 
| type value | message |
|------------|---------|
| 1          | SPEED   |
| 2          | GPS     |
| 3          | FUEL    |
 
Read byte 0 **first**. Then you know how to read the body. Not every packet has
the same shape, so you must check the type every time.
 
### Bodies (different for each type)
 
**SPEED (type 1)** — packet is 6 bytes
| bytes | meaning        | type      |
|-------|----------------|-----------|
| 2–5   | speed in km/h  | float (f) |
 
**GPS (type 2)** — packet is 10 bytes
| bytes | meaning     | type      |
|-------|-------------|-----------|
| 2–5   | latitude    | float (f) |
| 6–9   | longitude   | float (f) |
 
**FUEL (type 3)** — packet is 6 bytes
| bytes | meaning             | type                 |
|-------|---------------------|----------------------|
| 2–5   | fuel percent 0–100  | unsigned int 4B (I)  |
 
---
 
## The vehicle list (id → name)
 
The vehicle id (byte 1) means these ten vehicles. Copy this into your program (a
dict is a good choice). Use it to change ids into names on your screen.
 
| id | name              | kind  |
|----|-------------------|-------|
| 0  | Rusty Rocket      | van   |
| 1  | Silver Arrow      | car   |
| 2  | Sky Whale         | plane |
| 3  | Midnight Courier  | van   |
| 4  | Thunderbird       | plane |
| 5  | Green Machine     | car   |
| 6  | Iron Pigeon       | plane |
| 7  | Sandstorm         | van   |
| 8  | Blue Comet        | car   |
| 9  | Night Owl         | plane |
 
Easy way to check your work: the **planes drive about 750–820 km/h**. The vans
and cars are much slower, about **65–130 km/h**. So if "Sky Whale" shows 780,
your code is probably correct. If it shows a strange number like `1.4e-40`, it
is wrong (see the tips at the bottom).
 
---
 
## Worked examples (read these first!)
 
Here are three real packets, shown as **hex** (each `XX` is one byte). Follow
the decoding step by step. This shows you exactly what your program must do.
 
Note: `0x` just means "this is a hex number." For example, `0x03` is `3` in
normal (decimal) numbers, and `0x57` is `87`.
 
### Example 1 — a FUEL packet
 
```
03 05 00 00 00 57
```
 
- Byte 0 = `0x03` = **3** → message type 3 → this is a **FUEL** packet.
- Byte 1 = `0x05` = **5** → vehicle id 5 → **Green Machine**.
- Bytes 2–5 = `00 00 00 57` → this is the fuel, an unsigned int (4 bytes).
  Big-endian means the first byte is the biggest. Here the first three bytes are
  `00`, so only the last byte matters: `0x57` = 5×16 + 7 = 80 + 7 = **87**.
- **Result: Green Machine, fuel 87%.**
You unpack this whole packet with the format `">BBI"`. It gives you
`(3, 5, 87)`.
 
### Example 2 — a SPEED packet
 
```
01 01 42 F0 00 00
```
 
- Byte 0 = `0x01` = **1** → message type 1 → this is a **SPEED** packet.
- Byte 1 = `0x01` = **1** → vehicle id 1 → **Silver Arrow**.
- Bytes 2–5 = `42 F0 00 00` → this is the speed, a float (4 bytes).
- **Result: Silver Arrow, speed 120.0 km/h.**
You unpack this whole packet with the format `">BBf"`. It gives you
`(1, 1, 120.0)`.
 
A float is not a simple number like the fuel was. The 4 bytes follow a standard
(called IEEE 754), and `struct.unpack` turns them into the number for you. You
do **not** need to decode a float by hand — the `f` in the format does it.
 
(If you are curious how `42 F0 00 00` becomes 120.0: those bytes in binary are
`0 10000101 1110000...`. The middle part `10000101` is 133; minus 127 gives 6.
The last part means 1.875. So the value is 1.875 × 2⁶ = 1.875 × 64 = 120. Nice,
but again — `unpack` does all this for you.)
 
### Example 3 — a GPS packet
 
```
02 00 42 25 51 EC 41 9E 8F 5C
```
 
- Byte 0 = `0x02` = **2** → message type 2 → this is a **GPS** packet.
- Byte 1 = `0x00` = **0** → vehicle id 0 → **Rusty Rocket**.
- Bytes 2–5 = `42 25 51 EC` → the **first** float → latitude.
- Bytes 6–9 = `41 9E 8F 5C` → the **second** float → longitude.
- **Result: Rusty Rocket, latitude 41.33, longitude 19.82.**
You unpack this whole packet with the format `">BBff"` (two floats!). It gives
you `(2, 0, 41.33, 19.82)`.
 
The important thing here: a GPS packet is **longer** (10 bytes) because it has
two floats. Count carefully so you take bytes 2–5 for one and 6–9 for the other.
 
---
 
## The project has 4 parts
 
You will build this in **4 parts**. Each part adds on top of the one before it.
Finish one part and make it work before you start the next.
 
- **Part 1:** Read the data and show it live in the terminal.
- **Part 2:** Show the data in a web page (a list in the browser).
- **Part 3:** Show the vehicles moving on a Google map.
- **Part 4:** Save the history and draw the roads each vehicle traveled.
---
 
## Part 1 — Live terminal display (start here)
 
### Goal
A Python program that reads the packets and shows the **current** values of all
10 vehicles in the terminal. Not a long log — the screen should clear and only
show the newest values, like a real control board.
 
### What you need to work out
- A way to receive the packets arriving on port 50505.
- A way to turn the raw bytes back into real numbers (you already have the
  formats above).
- A way to remember the **most recent** values for each vehicle, so you can show
  all 10 at once instead of one packet at a time.
- A way to turn a vehicle id into its name.
(How you do each of these — which tools and which way to store the data — is
your decision. Part of the job is choosing.)
 
### Steps
1. **Receive something.** Open the socket and print the raw `data` bytes for
   each packet. You will see strange text like `b'\x01\x02D\x42...'`. That is
   correct — those are the real bytes. If you see them, your connection works.
2. **Read one type.** Handle only SPEED (type 1) first. Unpack it and print a
   real speed in km/h. Skip the rest.
3. **Check type + show name.** Read byte 0, handle all three types, and use the
   id to print the name: `Sky Whale SPEED: 781 km/h`, etc.
4. **Make it a live board.** Instead of printing a long list, keep only the
   newest values for each vehicle. Every time a packet arrives, clear the screen
   and print the full table again — one line per vehicle with speed, position,
   and fuel. (Tip to clear the screen: print `"\033[H\033[J"`.)
### Example of what the board could look like
 
The exact layout is up to you. This is just to show the idea — the newest values
for all 10 vehicles, redrawn in place so it updates live:
 
```
FLEET STATUS — 10 vehicles
------------------------------------------------------------------------
Rusty Rocket      SPEED    63 km/h   FUEL  96%   POS  41.2526,   19.8593
Silver Arrow      SPEED   112 km/h   FUEL  96%   POS  45.4582,    9.3145
Sky Whale         SPEED   785 km/h   FUEL  96%   POS  49.5846,    2.5595
Midnight Courier  SPEED    71 km/h   FUEL  95%   POS  52.5315,   13.3126
Thunderbird       SPEED   816 km/h   FUEL  96%   POS  50.8278,    0.3314
Green Machine     SPEED   125 km/h   FUEL  96%   POS  40.4949,   -3.8113
Iron Pigeon       SPEED   760 km/h   FUEL  96%   POS  56.5279,   37.6003
Sandstorm         SPEED    70 km/h   FUEL  96%   POS  30.0095,   31.3332
Blue Comet        SPEED   125 km/h   FUEL  95%   POS  35.5431,  139.6104
Night Owl         SPEED   793 km/h   FUEL  96%   POS  40.7988,  -74.7982
```
 
Notice the speeds match the vehicle kind — the planes (Sky Whale, Thunderbird,
Iron Pigeon, Night Owl) are near 800 km/h, the cars and vans are much slower. If
your board shows that, your parsing is working.
 
### Done when
The terminal shows a clean table of 10 vehicles, and the numbers change in real
time. No scrolling log — only the current values.
 
### Questions (answer these before Part 2)
Each question checks a concept. Answer in your own words.
 
1. Why must you read byte 0 (the type) **before** you can read the rest of the
   packet? What would go wrong if you always assumed every packet was 6 bytes?
2. What does **big-endian** mean at the level of individual bytes? In the FUEL
   example `00 00 00 57`, which byte is worth the most, and why?
3. If a temperature-style float came out as `1.4e-40`, what exactly did you get
   wrong, and why does that specific mistake produce a tiny number instead of an
   error?
4. A float and an unsigned int can both be 4 bytes on the wire. So how does your
   program know whether 4 bytes mean `120.0` or `1120403456`? What decides it?
5. Why is a GPS packet 10 bytes while a FUEL packet is 6? What in the format
   string causes that difference?
6. With UDP, how many messages does one `recvfrom` give you — never a half, never
   two stuck together? Why does that make your parsing simpler than it would be
   over a stream like TCP?
7. UDP does not guarantee delivery. If one packet is lost on the way to you, what
   happens on your side — an error, a wait, or nothing? How would you even notice?
8. You look up the vehicle name from the id byte. Why send a 1-byte id over the
   network instead of sending the text `"Sky Whale"` in every packet?
9. What is the difference between the raw `bytes` object you receive and the
   Python numbers you get after `struct.unpack`? What did `unpack` actually do?
10. Where does your program get the port number 50505 from, and what would happen
    if you listened on a different port than the sender is using?



## Part 2 — Web page with a list
 
Now you show the same data in a web browser instead of the terminal.
 
### Important idea (read this!)
A web browser **cannot read UDP packets**. It does not have a UDP socket. So you
cannot connect the browser straight to the vehicles.
 
The answer is to build **two programs**:
1. A **backend** (Python). It reads the UDP packets (the same code as Part 1)
   and keeps the newest data in memory, updated in real time. It also answers
   requests from the browser through an **API endpoint** — a web address the
   browser can call to get the current data.
2. A **frontend** (HTML + JavaScript in the browser) that gets the data from
   your endpoint and shows it on the page.
So the data flows like this:
 
```
vehicles → (UDP) → your Python backend → (over the web) → browser page
```
 
### What you need to work out
- A way for your Python backend to answer requests from a browser. (Python does
  not do this on its own — research what people use to serve a web API.)
- Your packet-reading from Part 1 has to keep running **at the same time** as the
  part that answers the browser, and both have to share the same live data. How
  you make two things run at once, and share data safely, is for you to solve.
- An endpoint that hands the browser the current data for all vehicles, in a
  form the browser's JavaScript can read.
### Steps
1. Bring your Part 1 packet-reading into the backend so it keeps running and
   keeps the newest values updated while the backend also serves the web.
2. Add an endpoint (for example `/data`) that returns the current values for all
   vehicles.
3. Open `/data` in your browser and check you see the data as text that changes
   when you refresh.
4. Build a web page that reads your endpoint and shows a list of the vehicles:
   **name, coordinates, speed, fuel**. How the page keeps the list up to date is
   for you to figure out.
### Done when
You open the page in a browser and see all 10 vehicles in a list, and the values
keep up with the real data.
 
### Questions (answer these before Part 3)
Each question checks a concept. Answer in your own words.
 
1. Why can a web browser **not** read the UDP packets directly? What can a browser
   speak to a server instead?
2. Your backend now does two jobs at once: receiving UDP and answering the
   browser. If you ran both in a single loop, one after the other, what would go
   wrong?
3. Both jobs touch the same live data — one writes it, the other reads it. What
   kind of bug can happen when two things use the same data at the same time, and
   how did you avoid it?
4. What is an **API endpoint**, really? When the browser "calls `/data`," what is
   physically being sent and sent back?
5. In what format does your endpoint send the data, and why is a structured text
   format better here than, say, sending your raw bytes to the browser?
6. Your endpoint replies with a *snapshot* — the current values at the moment it
   was asked. Why can't the endpoint instead "stay open" and keep sending new
   values as they arrive? (Think about how a normal web request works: ask,
   answer, done.)
7. The vehicles send data many times a second, but the browser only sees new
   numbers when it asks the endpoint again. So what decides how often the page
   updates — the sender's speed, or how often the browser asks?
8. Which parts of your system run on your machine, and which part runs on the
   computer of a person looking at the page? Draw the line between backend and
   frontend.
9. Your backend holds the latest values in memory (in a variable, not saved to
   disk). If the backend program crashes and you restart it, what happens to
   those values, and why?
10. Right now, to see new numbers the browser has to ask again. What is the
    browser doing to stay up to date, and what is one downside of that approach?


---
 
## Part 3 — Show the vehicles on a map (Google Maps)
 
Now put the vehicles on a real map, at their real coordinates, and let them move.
 
### What you need to work out
- A **Google Maps API key**. Google Maps needs a free key to work in a web page.
  This is the one thing you can't guess — search "Google Maps JavaScript API get
  API key". (Ask me — I can help set this up, or give you a key.)
- How to put a Google map on your page and place a point on it for each vehicle.
  (Google's map library can do both — research how.)
- A source for each vehicle's current position. Think about what you already
  built in Part 2.
### Steps
1. Add a map to your page centered on the middle of the fleet.
2. Place one point (a marker) for each vehicle at its current coordinates.
3. As new data comes in, **move each marker** to its new position. The vehicles
   will appear to drive.
4. Nice touch: show the vehicle name (and speed/fuel) when you click a marker.
### Done when
You see 10 markers on a real map, each with the right name, and they move on
their own as new data arrives.
 
### Questions (answer these before Part 4)
Each question checks a concept. Answer in your own words.
 
1. Why does Google Maps need an **API key**? What is the key actually for, from
   Google's point of view?
2. A marker needs to know where to appear. Which two numbers place it, and which
   packet type do they come from?
3. The map needs each vehicle's current position. You already built something in
   Part 2 that provides exactly that. What is it, and why does that mean the
   backend needs no changes for this part?
4. The map runs as JavaScript in the browser, but the vehicle data comes from
   your Python backend. How does a number that started as bytes over UDP end up
   moving a marker on screen? Trace the whole path.
5. To make a marker "move," do you create a new marker each update or change the
   existing one? What would go wrong if you did it the other way?
6. Latitude and longitude are just two numbers. How does the map turn them into a
   pixel position on the screen? (You don't need the math — explain the idea.)
7. The vehicle coordinates change by tiny amounts each update. Why does the
   marker still appear to move smoothly-ish, and what would make the movement look
   jumpy instead?
8. If the backend sent a latitude the map considers invalid (say, 999), what
   would you expect to see, and whose job is it to catch that — backend or
   frontend?
9. The API key sits in your HTML, which anyone visiting the page can read. Why is
   that a concern, and what do real sites do about it?
10. Nothing about the *sender* changed between Part 1 and Part 3 — the same bytes
    are on the wire. So what actually changed to get from a terminal to a live
    map? Name the layers you added.
---
