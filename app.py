from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    request,
    render_template,
    session,
    url_for,
)
from ai_model import get_ai_response
import pyrebase
from azure.cosmos import exceptions, CosmosClient
from dotenv import load_dotenv
from clu_sentiment import get_clu_sentiment
from datetime import datetime

load_dotenv()

app = Flask(__name__)

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
"""
firebase_api_key = os.getenv("FIREBASE_API_KEY")
firebase_auth_domain = os.getenv("FIREBASE_AUTH_DOMAIN")
firebase_database_url = os.getenv("FIREBASE_DATABASE_URL")
firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")
firebase_storage_bucket = os.getenv("FIREBASE_STORAGE_BUCKET")
firebase_messaging_sender_id = os.getenv("FIREBASE_MESSAGING_SENDER_ID")
firebase_app_id = os.getenv("FIREBASE_APP_ID")
firebase_measurement_id = os.getenv("FIREBASE_MEASUREMENT_ID")
"""

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

cosmos_uri = "https://emotiguard-database.documents.azure.com:443/"
cosmos_key = "j4sZto9VEgTVKvuFDpPGtWQBTla5DcvTd4YcLNSZUo7R9ZAcJKcM7dLYWhWjYWPTzChiTTLitFQCACDblM4Gfw=="
cosmos_client = CosmosClient(cosmos_uri, cosmos_key)
database_name = "emotiguard_db"
container_name = "conversations"
database = cosmos_client.get_database_client(database_name)
container = database.get_container_client(container_name)

CLU_ENDPOINT = "https://emotiguard-clu.cognitiveservices.azure.com/"
CLU_KEY = "5881bff47ca340ebabc85378c1730ec8"
PROJECT_NAME = "EmotiGuardluis"
DEPLOYMENT_NAME = "EmotiGuard_CLU"

app.secret_key = "secret"


@app.route("/", methods=["GET", "POST"])
def index():
    if "user" in session:
        return redirect(url_for("chat"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            # Authenticate the user with Firebase
            auth.sign_in_with_email_and_password(email, password)
            session["user"] = email
            return redirect(url_for("chat"))
        except:
            flash("Invalid email or password", "error")

    return render_template("signup.html")


# Route for signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user" in session:
        return redirect(url_for("chat"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            # Check if the email is already registered
            auth.get_account_info(email)
            flash("Email already registered. Please login.", "error")
            return redirect(url_for("login"))  # Redirect to the login page
        except:
            # If email is not registered, proceed with user registration
            auth.create_user_with_email_and_password(email, password)
            session["user"] = email
            # return redirect(url_for("details_form"))
            return redirect(url_for("chat"))

    return render_template("signup.html")


# Route for login
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("chat"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            # Authenticate the user with Firebase
            auth.sign_in_with_email_and_password(email, password)
            session["user"] = email
            return redirect(url_for("chat"))
        except:
            flash("Invalid email or password", "error")

    return render_template("login.html")


"""@app.route("/chat", methods=["GET", "POST"])
def chat():
    # Handle the form submission or any other logic for the chat page
    return render_template("chat.html")"""


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["user_input"]

        # Get CLU sentiment analysis
        sentiment_category = get_clu_sentiment(
            user_input,
            clu_endpoint=CLU_ENDPOINT,
            clu_key=CLU_KEY,
            project_name=PROJECT_NAME,
            deployment_name=DEPLOYMENT_NAME,
        )

        # Call the function that interacts with your AI model
        ai_response = get_ai_response(user_input, sentiment_category)

        # Perform any additional actions, such as saving to Cosmos DB
        # save_to_cosmos(user_input, ai_response, sentiment_category)

        return render_template(
            "chat.html",
            user_input=user_input,
            ai_response=ai_response,
            sentiment_category=sentiment_category,
        )

    return render_template("chat.html")


@app.route("/get_ai_response", methods=["POST"])
def get_ai_response_route():
    try:
        data = request.get_json()
        user_input = data.get("user_input")
        sentiment_category = get_clu_sentiment(
            user_input,
            clu_endpoint=CLU_ENDPOINT,
            clu_key=CLU_KEY,
            project_name=PROJECT_NAME,
            deployment_name=DEPLOYMENT_NAME,
        )
        # Call the function that interacts with your AI model
        ai_response = get_ai_response(user_input, sentiment_category)

        return jsonify({"ai_response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Function to insert sentiment into Cosmos DB
def insert_sentiment(user_id, sentiment_category):
    today_date = datetime.utcnow().date().isoformat()
    item = {
        "user_id": user_id,
        "date": today_date,
        "sentiment_category": sentiment_category,
    }
    container.upsert_item(item)


@app.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        # Perform logout actions
        session.pop("user", None)
        return render_template("login.html")
    else:
        # If it's a GET request, you may want to redirect to the login page
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
