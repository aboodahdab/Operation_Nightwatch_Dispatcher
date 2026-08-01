async function getData (){
const data=await fetch("/get_data")
const jsoned_data=await data.json()
console.log(jsoned_data)
} 
window.onload=getData()