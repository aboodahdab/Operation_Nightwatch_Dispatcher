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
## Part 3:
## Part 4:
