/* 
Handles the submission of registration data: when the button is clicked,
all form fields are read, any error messages are cleared, and the data is sent to the backend
via a POST request. The server’s response determines which warnings to display
(invalid email, weak password, empty fields, user already registered). If
registration is successful, a confirmation message is displayed and, after a short delay,
the user is redirected to the login page.
*/

document.getElementById('btnRgs').addEventListener('click', async () => {
    /*Let's reset warning errors */
    document.getElementById('emptyFieldsOrRegistered').textContent = "";
    document.getElementById('emailWarning').textContent = "";
    document.getElementById('passwordWarning').textContent = "";
    /*Let's get the values from fields */
    const email= document.getElementById('email').value;
    const password= document.getElementById('password1').value;
    const password1= document.getElementById('password2').value;
    const name= document.getElementById('name').value;
    const surname= document.getElementById('surname').value;
    const fiscal_code= document.getElementById('fiscalcode').value;
    const gender= document.getElementById('gender').value;
    const birthday= document.getElementById('birthday').value;
    /*Let's call the be */
    const res= await fetch('http://localhost:5000/registration', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, password1, name, surname, fiscal_code, gender, birthday})
    })
    /*Here the response */
    const data = await res.json();

    if (data.text === 'Empty fields.') {
        document.getElementById('emptyFieldsOrRegistered').textContent= data.text;
        document.getElementById('emptyFieldsOrRegistered').style.color= 'red';
    } else if(data.text === 'You have been registered!') {
        document.getElementById('emptyFieldsOrRegistered').textContent= data.text;
        document.getElementById('emptyFieldsOrRegistered').style.color= 'green';
        /*After un sec and half we will be redirected in the main page for the login*/
        setTimeout(() => {
            window.location.href = './main_page.html'
        }, 1500);

    } else if (data.text === 'Unvalid email') {
        document.getElementById('emailWarning').textContent= data.text;
        document.getElementById('emailWarning').style.color= 'red';
    } else if (data.text === 'Email already registered.') {
        document.getElementById('emailWarning').textContent= data.text;
        document.getElementById('emailWarning').style.color= 'red';
    } else if (data.text === 'Password is not strong enough.') {
        document.getElementById('passwordWarning').textContent= data.text;
        document.getElementById('passwordWarning').style.color= 'red';
    } else if (data.text === 'Passwords are not equal.'){
        document.getElementById('passwordWarning').textContent= data.text;
        document.getElementById('passwordWarning').style.color= 'red';
    } else if (data.text === 'Fiscal code is not correct.') {
        document.getElementById('fiscalCodeValidator').textContent= data.text;
        document.getElementById('fiscalCodeValidator').style.color= 'red';
    }

})

document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        document.getElementById("btnRgs").click();
    }
});