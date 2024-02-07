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
from clu_sentiment import get_clu_sentiment
from datetime import datetime
import os

app = Flask(__name__)


CLU_ENDPOINT = "https://emotiguard-clu.cognitiveservices.azure.com/"
CLU_KEY = "5881bff47ca340ebabc85378c1730ec8"
PROJECT_NAME = "EmotiGuardluis"
DEPLOYMENT_NAME = "EmotiGuard_CLU"

app.secret_key = "secret"


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("landing_page"))


@app.route("/landing_page")
def landing_page():
    return render_template("load.html")


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


"""# Function to insert sentiment into Cosmos DB
def insert_sentiment(user_id, sentiment_category):
    today_date = datetime.utcnow().date().isoformat()
    item = {
        "user_id": user_id,
        "date": today_date,
        "sentiment_category": sentiment_category,
    }
    container.upsert_item(item)
"""

if __name__ == "__main__":
    app.run(port=5000, debug=True)
