async function registerStudent(){

let name=document.getElementById("name").value
let roll=document.getElementById("roll").value

let res=await fetch("/register_student",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
name:name,
roll:roll
})

})

let data=await res.json()

document.getElementById("status").innerHTML=data.message

}


async function loadStudents(){

let res=await fetch("/get_students")

let data=await res.json()

let table=document.querySelector("#studentTable tbody")

if(!table) return

table.innerHTML=""

data.students.forEach(student=>{

let row=`
<tr>
<td>${student[0]}</td>
<td>${student[1]}</td>
<td><input type="checkbox" value="${student[0]}"></td>
</tr>
`

table.innerHTML+=row

})

}


async function saveAttendance(){

let checks=document.querySelectorAll("input[type='checkbox']:checked")

let names=[]

checks.forEach(c=>{
names.push(c.value)
})

let res=await fetch("/save_attendance",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({names:names})

})

let data=await res.json()

document.getElementById("status").innerHTML=data.message

}


async function loadToday(){

let res=await fetch("/get_attendance?type=today")

let data=await res.json()

showTable(data.attendance)

}


async function loadTotal(){

let res=await fetch("/get_attendance")

let data=await res.json()

showTable(data.attendance)

}


function showTable(rows){

let table=document.querySelector("#attendanceTable tbody")

table.innerHTML=""

rows.forEach(r=>{

let tr=`
<tr>
<td>${r[0]}</td>
<td>${r[1]}</td>
<td>${r[2]}</td>
</tr>
`

table.innerHTML+=tr

})

}


function downloadCSV(){

window.location="/download_csv"

}


if(document.getElementById("studentTable")){
loadStudents()
}