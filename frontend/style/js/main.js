const socket = io("http://localhost:4000/");
const body = document.body;
const ul = document.querySelector("ul");

let obj = {};

socket.on("Data", (data) => {
  key = Object.keys(data)[0];
  // the key serves as the car's id
  value = Object.values(data)[0];

  value2 = JSON.parse(value);
  type = Object.keys(value2)[0];
  data = Object.values(value2)[0];
  dataDecorater(key, type, data);
});

function get_name(index) {
  const names_array = [
    "Rusty Rocket",
    "Silver Arrow",
    "Sky Whale",
    "Midnight Courier",
    "Thunderbird",
    "Green Machine",
    "Iron Pigeon",
    "Sandstorm",
    "Blue Comet",
    "Night Owl",
  ];
  return names_array[index];
}

function print_result() {
  clearScreen();
  const entries = Object.entries(obj);
  for (i = 0; i < entries.length; i += 1) {
    const entry = entries[i];
    const key = entry[0];
    const value = entry[1];
    const valueLen = Object.entries(value).length;
    const naming = get_name(key);

    if (valueLen === 3) {
      const speed = value["SPEED"];
      const gps = value["GPS"];
      const fuel = value["FUEL"];
      const lat = gps[0];
      const lon = gps[1];
      const str = `${naming.padEnd(15)} SPEED ${String(speed).padStart(6)} km/h   FUEL ${String(fuel).padStart(4)}%   POS ${String(lat).padStart(9)}, ${String(lon).padStart(9)}`;
      addToScreen(str);
    }
  }
}
function clearScreen() {
  ul.innerHTML = "";
}
function dataDecorater(key, type, data) {
  if (!Object.hasOwn(obj, key)) {
    obj[key] = {};
  }

  const this_vehicle = obj[key];
  this_vehicle[type] = data;

  print_result();
}

function addToScreen(str) {
  const li = document.createElement("li");
  li.textContent = str;

  ul.appendChild(li);
}
