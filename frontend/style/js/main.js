const socket = io("http://localhost:4000/");
const body = document.body;
const ul=document.querySelector("ul")
console.log(ul)
let obj = {};

socket.on("connect", () => {
  // console.log("Connected to socket:", socket.id);
});
socket.on("Data", (data) => {
  key = Object.keys(data)[0];
  // the key serves as the car's id
  value = Object.values(data)[0];

  value2 = JSON.parse(value);
  type = Object.keys(value2)[0];
  data = Object.values(value2)[0];
  dataDecorater(key, type, data);
});
function dataDecorater(key, type, data) {


  if (!Object.hasOwn(obj, key)) {

    obj[key] = {};
  }

  const this_vehicle = obj[key];
  this_vehicle[type] = data;
  console.log("obj",obj)
  const li = document.createElement("li");
  li.textContent=`${key}:{${type}:${data}}`
  ul.innerHTML=""
  ul.appendChild(li);

}
