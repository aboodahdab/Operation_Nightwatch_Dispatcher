const socket = io("http://localhost:4000/");
const body = document.body;
const ul = document.querySelector("ul");
const mapElement = document.querySelector("gmp-map");

let obj = {};
let markerCount = 0;
function initMap() {
  // Get the inner map.
  const innerMap = mapElement.innerMap;

  // Set map options.
  innerMap.setOptions({
    mapTypeControl: false,
    zoom: 2,
  });
}

function newMarker(lat, lon, str, vehicleID) {
  const AdvancedMarkerElement = google.maps.marker.AdvancedMarkerElement;
  if (markerCount >= 10) {
    const marker = document.querySelector(
      `gmp-advanced-marker[data-name*="${vehicleID}"]`,
    );

    marker.position = { lat: lat, lng: lon };
    return;
  }
  const innerMap = mapElement.innerMap;
  const coords = { lat: lat, lng: lon };

  const marker = new AdvancedMarkerElement({
    map: innerMap,
    position: coords,
    title: str,
  });
  marker.dataset.name = vehicleID;
  markerCount += 1;
}
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

function print_result(k, t, d) {
  clearScreen();
  let needed_gps_str=""
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
      const str = `${naming} SPEED ${String(speed)} km/h   FUEL ${String(fuel)}%   POS ${String(lat)}, ${String(lon)}`;
      // if this is the same vehicle as the one we're checking change it's str value to this str 
      if (k===key){
     
        needed_gps_str=str
      }
      addToScreen(str);
      // Warning: If you put isItGPS() here ,it will repeat insanley and the markers will make an error.
    }
  }
  isItGPS(k, t, needed_gps_str, d);
}
function clearScreen() {
  ul.innerHTML = "";
}
function isItGPS(key, type, str, data) {
  if (type === "GPS") {
    const lat = data[0];
    const lon = data[1];

    newMarker(lat, lon, str, key);
  }
  return;
}
function dataDecorater(key, type, data) {
  if (!Object.hasOwn(obj, key)) {
    obj[key] = {};
  }
  const this_vehicle = obj[key];
  this_vehicle[type] = data;

  print_result(key, type, data);
}

function addToScreen(str) {
  const li = document.createElement("li");
  li.textContent = str;

  ul.appendChild(li);
}