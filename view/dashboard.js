/* 
Script that manages the dynamic behavior of the dashboard.
The loadSection function updates the central area by loading the HTML content
of the selected section and triggering the necessary functions
(e.g., loading appointments, medical records, profile).
Asynchronous functions communicate with the backend via fetch:
- sendAppointment sends a booking request.
- loadFutureAppointments and loadPastAppointments retrieve the patient’s
  future and past appointments.
- loadMedicalRecords retrieves medical records, generating an automatic
  visit if necessary.
- loadInformation loads profile data.
The logout function clears data saved in localStorage and redirects
the user to the home page.
*/


function loadSection(section) {
    const content = document.getElementById("content");

    switch(section) {
        case "new_appointment":
            content.innerHTML = `
                <h2>New appointment</h2>
                <p>Here, you can request a new appointment.</p>
                <p>Select a date:</p> <br>
                <input type="date" id="appointment" min= "2026-03-16">
                <button id="btnApt">Request</button>
                <p id="response"></p>


            `;

            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);

            const minDate = tomorrow.toISOString().split("T")[0];
            document.getElementById("appointment").setAttribute("min", minDate);

            document.getElementById('btnApt').addEventListener('click', sendAppointment);
            break;
            
        case "my_medical_record":
            content.innerHTML = `
            <h2>My medical record</h2>
            <p id="record-loading">Loading...</p>
            <div id="record-list"></div>
            `;
            loadMedicalRecords();
            break;

        case "future_appointments":
            content.innerHTML = `
                <h2>Future appointments</h2>
                <p id="future-loading">Loading...</p>
                <div id="future-list"></div>
            `;

            loadFutureAppointments();
            break;

        case "past_appointments":
            content.innerHTML = `
                <h2>Past appointments</h2>
                <p id='old-loading'>Loading...</p>
                <div id="old-list"></div>
            `;

            loadPastAppointments();
            break;

        case "profile":
            content.innerHTML = `
                <h2>Profile</h2>
                <p><strong>Email:</strong> <span id='email'></span></p>
                <p><strong>Name:</strong> <span id='name'></span></p>
                <p><strong>Surname:</strong> <span id='surname'></span></p>
                <p><strong>Gender:</strong> <span id='gender'></span></p>
                <p><strong>Fiscal code:</strong> <span id='fiscalCode'></span></p>
                <p><strong>Birthday:</strong> <span id='birthday'></span></p>
                
            `;

            loadInformation();
            break;
    }
}

function logout() {
    localStorage.clear();
    window.location.href = "./main_page.html";
};


async function sendAppointment() {
    const appointment = document.getElementById('appointment').value;
    const patient_id = localStorage.getItem('patient_id');

    if (!appointment) {
        document.getElementById('response').textContent = "Please select a date.";
        return;
    }

    const res = await fetch ("http://localhost:5000/appointments", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({ patient_id, appointment})

    })

    const data = await res.json();

    if (data.text === "Appointment added.") {
        document.getElementById('response').textContent= ''
        document.getElementById('response').textContent= data.text
    } else if (data.text === "No more slots available for this day.") {
        document.getElementById('response').textContent= ''
        document.getElementById('response').textContent= data.text
    } else if (data.text === "Appointment already exist.") {
        document.getElementById('response').textContent= ''
        document.getElementById('response').textContent= data.text
    }
}

async function loadFutureAppointments() {
    const patient_id = localStorage.getItem("patient_id");

    // Data di oggi in formato YYYY-MM-DD
    const today = new Date().toISOString().split("T")[0];

    const res = await fetch(`http://localhost:5000/future_appointments/${patient_id}/${today}`, {
        method: "GET",
    });

    const data = await res.json();
    console.log("APPOINTMENTS:", data.appointments);


    // Rimuove "Loading..."
    document.getElementById("future-loading").textContent = "";

    // Caso: nessun appuntamento.
    if (data.text === "You don't have any appointment.") {
        document.getElementById("future-list").innerHTML = `<p>${data.text}</p>`;
        return;
    }

    // Caso: appuntamenti trovati
    document.getElementById("future-list").innerHTML = `
        <ul>
            ${data.appointments.map(app => 
                 `
                <li>
                    <strong>Date:</strong> ${app.date_app} <br>
                    <strong>Time:</strong> ${app.time} <br>
                    <button class='btnDlt' onclick="deleteAppointment(${app.id})">Delete</button>
                </li>
                <br>
                <br>
            `).join("")}
        </ul>
    `;

}

async function loadPastAppointments () {
    const patient_id = localStorage.getItem("patient_id");
    
    // Data di oggi in formato YYYY-MM-DD
    const today = new Date().toISOString().split("T")[0];

    const res = await fetch(`http://localhost:5000/old_appointments/${patient_id}/${today}`, {
        method: "GET",   
    });

    const data = await res.json();

    // Rimuove "Loading..."
    document.getElementById("old-loading").textContent = "";

    // Caso: nessun appuntamento.
    if (data.text === "You don't have any appointment.") {
        document.getElementById("old-list").innerHTML = `<p>${data.text}</p>`;
        return;
    }

    // Caso: appuntamenti trovati
    document.getElementById("old-list").innerHTML = `
        <ul>
            ${data.appointments.map(app => `
                <li>
                    <strong>Date:</strong> ${app.date_app} <br>
                    <strong>Time:</strong> ${app.time} <br>
                    <strong>Doctor:</strong> ${app.doctor} <br>
                    <strong>Specialization:</strong> ${app.specialization} <br>
                </li>
                <br>
            `).join("")}
        </ul>
    `;

}

async function loadMedicalRecords() {
    const patient_id=localStorage.getItem('patient_id');
    const today = new Date().toISOString().split("T")[0];

    const res = await fetch (`http://localhost:5000/medical_records/${patient_id}/${today} `,{ 
        method: "GET"    
    });

    const data= await res.json();

    document.getElementById('record-loading').textContent=""
    if(data.text === 'No records registered yet.') {
        document.getElementById('record-list').innerText= data.text
        return;
        }
    document.getElementById('record-list').innerHTML=`
    <ul>
    ${data.records.map(rec => `
        <li>
            <strong>Diagnosis:</strong> ${rec.diagnosis}<br>
            <strong>Status:</strong> ${rec.status}
        </li>
        <br>
        `).join("")}
    </ul>
    `;
}

async function loadInformation() {
    const patient_id= localStorage.getItem('patient_id');
    const res = await fetch (`http://localhost:5000/info_profile/${patient_id}`,{ 
        method: "GET"    
    });
        
    
    const data = await res.json();
    
    document.getElementById('email').textContent= data.email;
    document.getElementById('name').textContent= data.name;
    document.getElementById('surname').textContent= data.surname;
    document.getElementById('gender').textContent= data.gender;
    document.getElementById('fiscalCode').textContent= data.fiscal_code;
    document.getElementById('birthday').textContent= data.birthday;
}

async function deleteAppointment(id) {
    const res = await fetch(`http://localhost:5000/dlt_appointment/${id}`, {
        method: "DELETE"
    });

    const data= await res.json();

    alert(data.text);

    loadFutureAppointments();
}