/* 
Handles user login: when the button is clicked, the email and password are retrieved,
sent to the backend via a POST request, and the response is analyzed. If
the credentials are incorrect, an error message is displayed; otherwise, the JWT token
and the patient ID are saved to localStorage, and the user is redirected
to the dashboard.
*/


document.getElementById('btnCred').addEventListener('click', async ()=> {
    const email= document.getElementById('email').value;
    const password = document.getElementById("password").value;

    const res = await fetch ('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })

    });

    const data = await res.json();
    
    if (data.text === 'Invalid credentials.') {
        document.getElementById('message').textContent= "Invalid credentials.";
        return;
    }

    localStorage.setItem('token', data.token);
    localStorage.setItem('patient_id', data.patient_id);
    

    window.location.href = "./dashboard.html";
    
})
