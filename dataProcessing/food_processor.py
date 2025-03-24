import requests
import os
from dotenv import load_dotenv
import json
from collections import defaultdict
import random
from datetime import datetime, timedelta

load_dotenv()

def return_random_date(start_date, end_date):
    # Calculate the difference between the two dates
    delta = end_date - start_date

    # Generate a random number of days within the range
    random_days = random.randint(0, delta.days)

    # Get the random date
    return start_date + timedelta(days=random_days)

def get_food_data(input_data):
    """
    Fetches food data from the USDA Food Data Central API based on the input query.
    """
    api_key = os.getenv("API_KEY")
    if api_key is None:
        return {"error": "API Key is missing"}

    # Extract the 'label' from input_data (assuming it's a dictionary with a 'label' key)
    if isinstance(input_data, dict) and "label" in input_data:
        query = input_data["label"]
    else:
        query = input_data

    api_url = (
        f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={query}"
    )

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}


def process_New_json(json_data):
    """
    Processes the JSON response from the USDA Food Data Central API and aggregates nutrient values,
    including the amount of sugar, and calculates a donation score.
    """
    # Check if the "foods" key exists in the response
    if "foods" not in json_data:
        print("Error: 'foods' key not found in the response.")
        print(f"Full JSON response: {json.dumps(json_data, indent=4)}")
        return {"error": "'foods' key not found in the API response"}

    # Initialize a dictionary to hold the sum of values by nutrient name
    nutrient_totals = defaultdict(float)

    for food in json_data["foods"]:
        for nutrient in food["foodNutrients"]:
            nutrient_name = nutrient["nutrientName"]
            value = nutrient["value"]
            nutrient_totals[nutrient_name] += value

    # Extract relevant nutrients
    protein = nutrient_totals.get("Protein", 0)
    fiber = nutrient_totals.get("Fiber, total dietary", 0)
    carbohydrates = nutrient_totals.get("Carbohydrate, by difference", 0)
    sugars = nutrient_totals.get("Sugars, total", 0)
    calories = nutrient_totals.get("Energy", 0)

    protein_factor = protein / 50 if protein < 50 else 1.0
    fiber_factor = fiber / 30 if fiber < 30 else 1.0
    carb_factor = (carbohydrates - sugars) / 100 if (carbohydrates - sugars) > 0 else 0
    calorie_factor = 1 - (calories - 50) / (350 - 50) if 50 <= calories <= 350 else 0
    perishability_factor = 0

    # Assign weights to factors
    W_p = 0.3
    W_f = 0.2
    W_c = 0.2
    W_cal = 0.2
    W_per = 0.1

    # Calculate final score
    donation_score = round(
        (
            W_p * protein_factor
            + W_f * fiber_factor
            + W_c * carb_factor
            + W_cal * calorie_factor
            - W_per * perishability_factor
        )
    )

    print(f"Donation score: {donation_score}")

    # Prepare the new JSON structure with score
    result = {
        "item": json_data["foodSearchCriteria"]["generalSearchInput"],
        "category": (
            json_data["foods"][0]["foodCategory"] if json_data["foods"] else "Unknown"
        ),
        "expiry_time": datetime.strftime(return_random_date(datetime.now(), datetime(2024, 10, 10)), '%Y-%m-%d %H:%M'),
        "donation_score": int(donation_score * random.uniform(5, 15)),
    }

    output = json.dumps(result, indent=4)
    return output


def process_food_data(food_item):
    """
    Processes the nutrient data of a given food item and returns a summary JSON.
    """
    food_data = get_food_data(food_item)

    # Check if the API returned a valid response
    if "error" in food_data:
        return food_data

    result = process_New_json(food_data)
    return result


if __name__ == "__main__":
    input_data = "orange"
    process_food_data(input_data)
