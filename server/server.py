

from flask import Flask, request, jsonify
from app_oop import FoodQuestDB
from flask_cors import CORS
import sys
import os
import io


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dataProcessing.food_processor import process_food_data 
from cv_data.testing import run_prediction
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
load_dotenv()

databaseName = os.getenv("DATABASE_NAME")
databasePass = os.getenv("PASSWORD")

if not databaseName or not databasePass:
    raise ValueError("Database name or password not found. Check your .env file.")

db = FoodQuestDB(databaseName, "anushka", "localhost", 3306, databasePass)




def predict_image(base64):
    model_output = run_prediction(base64)
    print(f"Model predicted: {model_output}")
    return process_food_data(model_output)

@app.route("/save-image", methods=['POST'])
def send_image():
    data = request.json
    base64_image = data.get('imageData')

    if not base64_image:
        return jsonify({"error": "No image data provided"}), 400

    return predict_image(base64_image)


@app.route("/get-all-users")
def get_all_users():
    users = db.get_users_ordered_by_points()
    return jsonify(users)


@app.route("/get-username/<int:user_id>")
def get_username_route(user_id):
    username = db.get_username(user_id)
    print(f"Fetching username for user_id {user_id}: {username}")  # Debugging line
    if username:
        return jsonify(username)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/get-user-data/<int:user_id>")
def get_user(user_id):
    submissions = db.food_submission_times_of_user(user_id)
    return jsonify(submissions)


@app.route("/insert-food", methods=['POST'])
def insert_food():
    data = request.json  # This will automatically parse JSON
    if not data:
        return jsonify({"error": "No JSON data found in request"}), 400

    ml_json = data.get("mlJson")
    if not ml_json or not all(k in ml_json for k in ["item", "donation_score", "expiry_time"]):
        return jsonify({"error": "Invalid data format"}), 400

    print(f"Request data: {ml_json}")
    db.insert_food(ml_json['item'], ml_json['donation_score'], ml_json['expiry_time'], 1)
    return jsonify({"message": "Successfully added food item to database"})

@app.route("/")
def home():
    return jsonify({"message": "Server is running!"})

@app.route("/test-db-connection")
def test_db_connection():
    try:
        # Simple check if the connection is open
        if db.connection.is_connected():
            return jsonify({"message": "Database connection successful!"})
        else:
            return jsonify({"error": "Database connection failed!"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
