const socket = io("http://localhost:4000/");
// async function getData() {
//   const data = await fetch("/get_data");
//   const jsoned_data = await data.json();
//   console.log(jsoned_data);
// }
console.log("hi")
socket.on("connect",()=>{
    console.log("ali",socket.id)
})
socket.on("Data",(data)=>{
console.log("whyy")

console.log(data,"data ()")
})

// window.onload = getData();
