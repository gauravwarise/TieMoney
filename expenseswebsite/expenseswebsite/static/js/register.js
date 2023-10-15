// console.log("register working");
const usernameField = document.querySelector('#usernameField')
const feedBackArea = document.querySelector(".invalid_feedback")
const showPassword = document.getElementById("showPassword");
const submitbtn = document.querySelector(".submit-btn")
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const password = document.querySelector("#passwordField")
const confpassword = document.querySelector("#confirmPasswordField")
const notificationArea = document.querySelector(".password_missmatch")


usernameField.addEventListener("keyup", (e) =>{
    // console.log(usernameField.innerHTML());
    console.log("typing.......");
    const usernameVal = e.target.value;
    console.log('username is  => ', usernameVal.length);
    if(usernameVal.length>0){
        console.log("inside if ======================");
        fetch("/authentication/validate_username",{
            body:JSON.stringify({username:usernameVal}),
            // body:{username:usernameVal},
            method:"POST",
        })
        .then((res)=>res.json())
        .then((data)=>{
            console.log("data", data);
            if(data.username_error){
                submitbtn.disabled = true;
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display = 'block';
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`
            }else{
                submitbtn.removeAttribute("disabled");
                usernameField.classList.add("is-valid");
                feedBackArea.style.display = 'block';
                feedBackArea.innerHTML = `<p></p>`
            }
        });
    }
});


var emailVal;
emailField.addEventListener("keyup", (e)=>{
    const emailVal = e.target.value;
    console.log('email is  => ', emailVal.length);
    emailFeedBackArea.style.display = "none"
    if(emailVal.length>0){
        console.log("inside if ======================");
        fetch("/authentication/validate_email",{
            body:JSON.stringify({email:emailVal}),
            // body:{email:emailVal},
            method:"POST",
        })
        .then((res)=>res.json())
        .then((data)=>{
            console.log("data", data);
            if(data.email_error){
                submitbtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display = 'block';
                emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`
            }else{
                submitbtn.removeAttribute("disabled");
                emailField.classList.add("is-valid");
                emailFeedBackArea.style.display = 'block';
                emailFeedBackArea.innerHTML = `<p></p>`
            }
        });
    }
})

var passwordVal;w
password.addEventListener("keyup", (e)=>{
    passwordVal = e.target.value;
    console.log(passwordVal);
});
var confPasswordVal;
confpassword.addEventListener("keyup", (e)=>{
    confPasswordVal = e.target.value;
    console.log(confPasswordVal);
    console.log(confPasswordVal==passwordVal);
    if (confPasswordVal!=passwordVal) {
        notificationArea.style.display = 'block';
        notificationArea.innerHTML = `<p>Password doesnt match'</p>`        
    }else{
        notificationArea.style.display = 'block';
        notificationArea.innerHTML = `<p>Password match</p>`
        setTimeout(function(){
            notificationArea.textContent = "";
        },2200);
    }
});


showPassword.addEventListener("click", function() {
    if((password.type ==="password") || (confpassword.type === "password")){
        password.type = "text";
        confpassword.type ="text";
    }else{
        password.type = "password";
        confpassword.type ="password";
    }
})
console.log("=======",passwordVal);


// submitbtn