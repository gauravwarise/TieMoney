// console.log("register working");
const usernameField = document.querySelector('#usernameField')
const feedBackArea = document.querySelector(".invalid_feedback")

const emailField = document.querySelector("#emailField");
const submitBtn = document.querySelector(".submit-btn");

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
  
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";
  
    if (emailVal.length > 0) {
      fetch("/authentication/validate-email", {
        body: JSON.stringify({ email: emailVal }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("data", data);
          if (data.email_error) {
            submitBtn.disabled = true;
            emailField.classList.add("is-invalid");
            emailFeedBackArea.style.display = "block";
            emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
          } else {
            submitBtn.removeAttribute("disabled");
          }
        });
    }
  });
console.log("yooooooooooooooooooo");
  

function redirectToLogin() {
    window.location.href = "{% url 'login' %}";
}
  




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
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display = 'block';
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`
            }else{
                usernameField.classList.add("is-valid");
                feedBackArea.style.display = 'block';
                feedBackArea.innerHTML = `<p></p>`
            }
        });
    }
});

const password = document.querySelector("#passwordField")
var passwordVal;
password.addEventListener("keyup", (e)=>{
    passwordVal = e.target.value;
    console.log(passwordVal);
});
const confpassword = document.querySelector("#confirmPasswordField")
const notificationArea = document.querySelector(".password_missmatch")
var confPasswordVal;
confpassword.addEventListener("keyup", (e)=>{
    confPasswordVal = e.target.value;
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

const showPassword = document.getElementById("showPassword");

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