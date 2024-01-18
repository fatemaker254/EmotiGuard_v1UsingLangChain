import pyrebase

config = {
    "apiKey": "AIzaSyCjPBwZOR_MJg2ZFJ2s9fYhti8MgHJ1oww",
    "authDomain": "login-with-firebase-data-d46f3.firebaseapp.com",
    "databaseURL": "https://login-with-firebase-data-d46f3-default-rtdb.firebaseio.com",
    "projectId": "login-with-firebase-data-d46f3",
    "storageBucket": "login-with-firebase-data-d46f3.appspot.com",
    "messagingSenderId": "63418211106",
    "appId": "1:63418211106:web:b0e5ea7190529f0418637b",
    "measurementId": "G-BQBX7MDESP",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = "test@gmail.com"
password = "test123"
# user = auth.create_user_with_email_and_password(email, password)
# print(user)

user = auth.sign_in_with_email_and_password(email, password)

# info = auth.get_account_info(user['idToken'])
# print(info)

# auth.send_email_verification(user['idToken'])
auth.send_password_reset_email(email)
