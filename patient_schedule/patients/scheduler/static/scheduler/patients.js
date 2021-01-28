document.body.onload = () => {
    getPatients()
}

const aptBtn = document.getElementById('apt-btn')
const bookBtn = document.getElementById('book-btn')
const patientTable = document.getElementById('patient-table')
const token = document.getElementById('patientForm').elements["csrfmiddlewaretoken"].value
const modal = document.getElementById('modal')

aptBtn.onclick = () => {
    form = document.querySelector('.patient-form-container')
    form.classList.toggle('hide')
}

bookBtn.onclick = (e) =>{
    e.preventDefault()
    makeAppointment()
}


async function makeAppointment(){

    
    const name = document.getElementById('id_name').value
    const aptDate = document.getElementById('id_appointment_date').value
    const aptTime = document.getElementById('id_appointment_time').value
    
    const response = await fetch(`/schedule/get_api/`,{
        method: 'POST',
        headers:{
            'X-CSRFToken':token,
            'Content-type': 'application/json',
        },
        body:JSON.stringify({
            name: name,
            appointment_date: aptDate,
            appointment_time: aptTime
        })

    })

    const data = await response.json()

    getPatients()

    
}


async function getPatients(){
    patientTable.innerHTML=``
    const response = await fetch(`/schedule/get_api/`)
    const data = await response.json()
    data.forEach(patient => {
        patientTable.innerHTML += `
        <tr>
            <th scope="row"></th>
            <td>${patient.name}</td>
            <td>${patient.appointment_time}</td>
            <td>${patient.appointment_date}</td>
            <td ><a data-pk="${patient.id}" href="#" class="edit-link btn btn-outline-success">☑️</a></td>
            <td ><a data-id="${patient.id}" href="#" class="del-link btn btn-outline-danger">❌</a></td>
        </tr>
        
        `
    })
    setEditLinks()
    setDeleteLinks()

    
}

function setDeleteLinks(){
    let delLinks = Array.from(document.querySelectorAll('.del-link'))

    delLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            deletePatient(e.target.dataset.id)
        }),
        {once: true}
    })
}

function setEditLinks(){
    let editLinks = Array.from(document.querySelectorAll('.edit-link'))

    editLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            let id = e.target.dataset.pk
            
            modal.classList.toggle('hide')
            displayPatientData(e.target.dataset.pk)
        
            
        }),
        {once: true}
    })
}

async function deletePatient(id){
    
    const response = await fetch(`/schedule/get_api/${id}/`,{
        method: 'DELETE',
        headers:{
            'X-CSRFToken':token,
            'Content-type': 'application/json',
        },

    })

    // const data = await response.json()
    // console.log(data)
    getPatients()

}

document.getElementById('closeModal').onclick = (e) => {
    modal.classList.toggle('hide')
}


async function displayPatientData(id) {
    const response = await fetch(`/schedule/get_api/${id}`)
    const data = await response.json()
    console.log(data)

    document.getElementById('edit-name').value = data.name
    document.getElementById('edit-date').value = data.appointment_date
    document.getElementById('edit-time').value = data.appointment_time
    document.getElementById('saveModal').dataset.num = data.id

}

document.getElementById('saveModal').onclick = (e)=>{
    savePatientEdit(e.target.dataset.num)
}
async function savePatientEdit(id){

    const response = await fetch(`/schedule/get_api/${id}/`,{
        method: 'PUT',
        headers:{
            'X-CSRFToken':token,
            'Content-type': 'application/json',
        },
        body:JSON.stringify({
            name: document.getElementById('edit-name').value,
            appointment_date: document.getElementById('edit-date').value,
            appointment_time: document.getElementById('edit-time').value
        })

    })

    const data = await response.json()
    getPatients()
    modal.classList.toggle('hide')

}