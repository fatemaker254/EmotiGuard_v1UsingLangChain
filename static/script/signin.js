// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCjPBwZOR_MJg2ZFJ2s9fYhti8MgHJ1oww",
  authDomain: "login-with-firebase-data-d46f3.firebaseapp.com",
  databaseURL: "https://login-with-firebase-data-d46f3-default-rtdb.firebaseio.com",
  projectId: "login-with-firebase-data-d46f3",
  storageBucket: "login-with-firebase-data-d46f3.appspot.com",
  messagingSenderId: "63418211106",
  appId: "1:63418211106:web:b0e5ea7190529f0418637b",
  measurementId: "G-BQBX7MDESP"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth();

//----- Registration code start
document.getElementById("registerForm").addEventListener("submit", function (e) {
  e.preventDefault();
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;

  // For new registration
  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      console.log(user);
      alert("Registration successfully!!");
      // Redirect to another page or perform other actions as needed
      window.location.href = 'app.html';
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      console.log(errorMessage);
      alert("Signup failed. Please check your email and password.");
    });
});
//----- Registration code end
