# Answers of TASK.md:
## Part 1:
## "Why must you read byte 0 (the type) before you can read the rest of the packet? What would go wrong if you always assumed every packet was 6 bytes?":
### Because you won't know if this is a gps,speed,or fuel packet You won't be able to parse them, for example the gps packet is 10 bytes and it contains latitiude and longitiude, how would you know that this is a gps packet and it contains latitude and longititude if you haven't read the first byte (the type)
## "What does big-endian mean at the level of individual bytes? In the FUEL example 00 00 00 57, which byte is worth the most, and why?": 
### Big-endian means to read the binary data from left to right so first byte will be 00 then 00 next is 00 then finally 57 for ```000057```   .The most worthy byte is the first byte because it has the most value.
## "If a temperature-style float came out as 1.4e-40, what exactly did you get wrong, and why does that specific mistake produce a tiny number instead of an error?" 
### I think you read a float in a integer format. Because it's a formatting issue and not a full error (I think)
## "A float and an unsigned int can both be 4 bytes on the wire. So how does your program know whether 4 bytes mean 120.0 or 1120403456? What decides it?" The program does NOT know that this is a float or an unsigned int instead, you gotta format the 4 bytes with float format or int format. and that is what decides it.
### We will first go through what does each one include.  the fuel and gps both include the packet type (first byte) + the vehicle id (second byte).But the fuel packet includes just one unsigned integer (4 bytes) so it becomes 6 bytes (1+1+4)=6. but the gps packet includes 2 integers so it's a (1+1+4+4)= 10
## "With UDP, how many messages does one recvfrom give you — never a half, never two stuck together? Why does that make your parsing simpler than it would be over a stream like TCP?"
### recvfrom gives you only one message or one packet at a time.because you won't need to handle the more cases of having multiple at the same time (like having to get each packet from an array I mean having an array of packets).
## "UDP does not guarantee delivery. If one packet is lost on the way to you, what happens on your side — an error, a wait, or nothing? How would you even notice?":
### Nothing. If packet is lost UDP ignores it. "How would you even notice? ": You won't probably but the downloaded file won't work or a frame will be missing from a video call. 
## "You look up the vehicle name from the id byte. Why send a 1-byte id over the network instead of sending the text "Sky Whale" in every packet?":
### Lower capacity I guess?.Just sending a one byte id needs less than 9 bytes (1 byte for each letter)
## "What is the difference between the raw bytes object you receive and the Python numbers you get after struct.unpack? What did unpack actually do?":
### struct.unpack transforms binary into letters or numbers depending on the format you give it. The difference is that the raw bytes are 8 bits each (that are only zeros 0 and ones 1) but the python numbers are daily used numbers from 0-9.
## "Where does your program get the port number 50505 from, and what would happen if you listened on a different port than the sender is using?": 
### The program get's the port from the sender (server) because it sends data on port 50505 specifically so the receiver and sender must agree on the port used.
### And if listening on another port,you could get data sent another server or get absolutely nothing (depending if there is another server using that port)

## Part 2:
## "Why can a web browser not read the UDP packets directly? What can a browser speak to a server instead?""
### Cuz the browser does not have a UDP socket. So it cannot read the UDP packets directly. 
## "Your backend now does two jobs at once: receiving UDP and answering the browser. If you ran both in a single loop, one after the other, what would go wrong?"
### If you run both in a single loop then the first will keep working forever so the second won't even have a chance to start (that is because the program does not stop and it needs to stop to let the loop go to the second program)
### "Both jobs touch the same live data — one writes it, the other reads it. What kind of bug can happen when two things use the same data at the same time, and how did you avoid it?"
## There is a bug that happens when a program reads and other writes at the same exact time (I think it's simply that the DATA CHANGES while the reading process is still working)
## "What is an API endpoint, really? When the browser "calls /data," what is physically being sent and sent back?"
### So. An API endpoint is an instruction for a port. when someone calls /data for example it returns {"foo":123} for example and what's getting sent is the method type and the endpoint (for exapmle GET and /data) what's getting sent back is the data (or whatever does the api endpoint return)
## "In what format does your endpoint send the data, and why is a structured text format better here than, say, sending your raw bytes to the browser?"
### It sends them in JSON. because let's just say that we will have to re-decode these packets. and that is performance and time wasting
## "Your endpoint replies with a snapshot — the current values at the moment it was asked. Why can't the endpoint instead "stay open" and keep sending new values as they arrive? (Think about how a normal web request works: ask, answer, done.)"
### I think it does because I used web sockets but the original TASK.md uses polling and needs to call the API endpoint every 5 seconds.
## "The vehicles send data many times a second, but the browser only sees new numbers when it asks the endpoint again. So what decides how often the page updates — the sender's speed, or how often the browser asks?"
### First of all,because we used web sockets we don't have to encounter this. 
### Second of all I think it updates when the browser asks to. Think of it, imagine having the data go into redis then flask gets it and it gets put in the data array but never sent to the browser. So the one controlling the refresh times is the browser. But with web sockets (our case) the one controlling the refresh times is the backend.
## "Which parts of your system run on your machine, and which part runs on the computer of a person looking at the page? Draw the line between backend and frontend."
### Firstly, the sender + receiver + Redis + Flask (the API handler) + the sending socket, all run on my machine. But the websocket listening for sent data runs on the user's machine and the frontend (HTML,CSS,Js) runs at the user's machine
### We have two parts of the socket here. The sender (flask socketio) and the listener , (Js socketio) listens for updates, runs on the user's own machine.
## "Your backend holds the latest values in memory (in a variable, not saved to disk). If the backend program crashes and you restart it, what happens to those values, and why?"
### They will vanish! Because variables live in ram and ram restarts whenever you start the program. But files live on the disk (ssd or nvme storage) and they are saved so if you restart your program they don't disappear.
## "Right now, to see new numbers the browser has to ask again. What is the browser doing to stay up to date, and what is one downside of that approach?"
### As I said that was before using web sockets.
### It was calling the API every 5 seconds and the downsides are that it uses more data (internet) and uses more cpu cycles (inefficent) I guess. + annoying the API.

## Part 3:
## "Why does Google Maps need an API key? What is the key actually for, from Google's point of view?"
### To track user's usage and know if they have reached the limit.
### "A marker needs to know where to appear. Which two numbers place it, and which packet type do they come from?"
### Latitude and longitude.
### They come from the GPS packet (index 1)
## "The map needs each vehicle's current position. You already built something in Part 2 that provides exactly that. What is it, and why does that mean the backend needs no changes for this part?"
### We built the Flask server connected to Redis in Part 2 that sends data to the frontend so we don't need to edit anything with the backend for this part.
## "The map runs as JavaScript in the browser, but the vehicle data comes from your Python backend. How does a number that started as bytes over UDP end up moving a marker on screen? Trace the whole path."
### the fleet server sends data to port 127.0.0.1 (localhost) then the main receives it and puts it in a .json file then we take the sent data and  dump it into redis next redis sends flask the data and flask sends it to the user using web sockets.
## "To make a marker "move," do you create a new marker each update or change the existing one? What would go wrong if you did it the other way?"
### I change the exisiting one's position
### I think both work.
## "Latitude and longitude are just two numbers. How does the map turn them into a pixel position on the screen? (You don't need the math — explain the idea.)"
### Latitude is the vertical line and longitude is the horizontal line, latitude tells us if the area is in the south/north and longtitude is for east/west 
### together they define a point. Example: latitude 30 (north of the equator by 30) and longitude 40 (east of the prime medrian by 40)
## "The vehicle coordinates change by tiny amounts each update. Why does the marker still appear to move smoothly-ish, and what would make the movement look jumpy instead?"
### Moving very fast will make the marker almost teleport and having a bad internet connection or having a slow server makes it also look jumpy.
## "If the backend sent a latitude the map considers invalid (say, 999), what would you expect to see, and whose job is it to catch that — backend or frontend?"
### then the marker will end up in the arctic ocean at the very north of the map. above Russia green land and canada.
### And I think it's the frontend's job to handle this.
## "The API key sits in your HTML, which anyone visiting the page can read. Why is that a concern, and what do real sites do about it?"
### Because anyone visitng the website can see it, copy it, use it, and you will need to pay because it's YOUR KEY.
### Real sites limit their API key for their domain only. For example "nightwatch.dispatcher.dev"
## "Nothing about the sender changed between Part 1 and Part 3 — the same bytes are on the wire. So what actually changed to get from a terminal to a live map? Name the layers you added." 
### We added a reciver that recied data from the sender then we added redis and flask. Redis's job is to take the data from the reciver and give it to flask next flask sends data to the frontend using a web socket.
## Part 4: Coming soon
