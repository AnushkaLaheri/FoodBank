from flask import Flask, request, jsonify
from app_oop import FoodQuestDB
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dataProcessing.food_processor import process_food_data 
from cv_data.testing import run_prediction
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
load_dotenv()
databaseName = os.getenv("DATABASE_NAME")
databasePass = os.getenv("PASSWORD")
db = FoodQuestDB(databaseName, "anushka", "localhost", 3306, databasePass)




def predict_image(base64):
    model_output = run_prediction(base64)
    print(f"Model predicted: {model_output}")
    return process_food_data(model_output)

@app.route("/save-image", methods=['POST'])
def send_image():
    data = request.json
    base64_image = data.get('imageData')
    return predict_image(base64_image)

@app.route("/get-all-users")
def get_all_users():
    users = db.get_users_ordered_by_points()
    return jsonify(users)


@app.route("/get-username/<int:user_id>")
def get_username_route(user_id):
    username = db.get_username(user_id)
    return jsonify(username)


@app.route("/get-user-data/<int:user_id>")
def get_user(user_id):
    submissions = db.food_submission_times_of_user(user_id)
    return jsonify(submissions)

@app.route("/insert-food", methods=['POST'])
def insert_food():
    data = request.json
    data = data["mlJson"]
    print(f"request: {data}")
    #request: {'mlJson': {'item': 'milk', 'expiry_time': '2024-10-03 02:09:34.657517', 'donation_score': 1}}
    db.insert_food(data['item'], data['donation_score'], data['expiry_time'], 1)
    return {"message": "Successfully added food item to database"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
