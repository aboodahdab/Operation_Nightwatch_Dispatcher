const socket = io("http://localhost:4000/");
const body = document.body;
const ul = document.querySelector("ul");
const mapElement = document.querySelector("gmp-map");

let obj = {};
let markerCount = 0;
let polylineCounter = 0;
let polylines = {};
function initMap() {
  // Get the inner map.
  const innerMap = mapElement.innerMap;

  // Set map options.
  innerMap.setOptions({
    mapTypeControl: false,
    zoom: 2,
  });
}
function drawAPolyline(key, coords) {
  if (polylineCounter >= 10) {
    console.log("polyline counter", polylines[key], coords);
    const used_poly = polylines[key];
    used_poly.setPath(coords); // force redraw

    return;
  }
  const innerMap = mapElement.innerMap;

  const flightPath = new google.maps.Polyline({
    path: coords,
    geodesic: true,
    strokeColor: "#FF0000",
    strokeOpacity: 1.0,
    strokeWeight: 2,
    map: innerMap,
  });
  if (Object.hasOwn(polylines, key)) {
    console.log(polylines);

    return;
  }
  polylines[key] = flightPath;
  console.log(polylines);
  polylineCounter += 1;
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
  // console.log(data);
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

function order_data(k, t, d) {
  clearScreen();
  let needed_gps_str = "";
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
      let isItRed = false;
      // if this is the same vehicle as the one we're checking change it's str value to this str
      if (k === key) {
        needed_gps_str = str;
      }
      if (fuel < 15) {
        isItRed = true;
      }
      addToScreen(str, isItRed);
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

  order_data(key, type, data);
}

function addToScreen(str, isItRed) {
  const li = document.createElement("li");

  li.textContent = str;
  if (!isItRed) {
    ul.appendChild(li);
    return;
  }
  li.style.color = "red";
  ul.appendChild(li);
}
async function order_history(packet) {
  let file_content = await read_file();
  const vehicleID = Object.keys(packet);
  const value = JSON.parse(Object.values(packet));
  const obj = { lat: value[0], lng: value[1] };
  // console.log(obj, obj);
  if (!Object.hasOwn(file_content, vehicleID)) {
    file_content[vehicleID] = [obj];
  } else {
    const arr = file_content[vehicleID];

    arr.push(obj);
  }
  gather_data(file_content);
  write_to_file(file_content);
}
function gather_data(data) {
  for (const [key, value] of Object.entries(data)) {
    drawAPolyline(key, value);
  }
}
socket.on("History_Data", async (data) => {
  await order_history(data);
});

async function write_to_file(query) {
  const response = await fetch("/write_to_history_file", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: query }),
  });
  if (!response.ok) {
    throw new Error("write history file fetch have FAILED");
  }
  const jsoned_response = await response.json();

}

async function read_file() {
  const response = await fetch("/read_history_file");
  if (!response.ok) {
    throw new Error("read history file fetch have FAILED");
  }
  const jsoned_data = await response.json();

  return jsoned_data;
}
