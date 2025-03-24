# FoodBank AI: Gamified Food Bank Web App

## Overview

FoodBank AI is a gamified web application designed to encourage food donations by allowing users to donate items, track their contributions, and earn points based on the nutritional value of the donated items. The application uses a combination of technologies including computer vision for food item recognition, a backend with a Postgres database, and an interactive React frontend. Users can see their rankings on a leadership board, motivating them to donate more.

## Features

- **Object Recognition**: Utilizes a computer vision (CV) model to identify food items from images uploaded by users.
- **Nutrient Analysis**: Integrates with the USDA Food Data Central API to fetch nutritional information based on recognized food items.
- **Leadership Board**: Tracks users' points based on their food donations. Points are calculated using the nutritional value of donated items.
- **Gamification**: Users earn points for every donation and can see their rankings on the leadership board, making the donation process fun and engaging.


## Using the App
- Donate Food: Upload a picture of the food item you want to donate. The app will recognize the item and calculate its nutritional value.
- Check Leadership Board: See how you rank among other donors based on the total points earned.
- Earn Points: The more nutritious the donated food, the higher the points!

## Technologies Used

- **Backend**:
  - **Python**: Data processing and API integration for food nutrient data.
  - **PostgreSQL**: Database for storing user data, donation history, and leadership board information.

- **Frontend**:
  - **React**: Front-end framework for building a responsive and interactive user interface.

- **Computer Vision**:
  - **CV Model**: Used for food item recognition from uploaded images. Models like `YOLO` or `ResNet` can be utilized for object detection.

- **APIs**:
  - **USDA Food Data Central API**: For fetching detailed nutritional information of recognized food items.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/foodquest.git
cd foodquest
```

### 2. Python Virtual Environment
```python
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Higher Level Figma View
figma: https://www.figma.com/design/dUoJU0oRnXrQ93cjLsSwvs/Untitled?embed-host=share&kind=file&node-id=0-1&page-selector=1&theme=light&version=2&viewer=1
![image](https://github.com/user-attachments/assets/6d619d10-159f-4257-9ae6-7b7ff851550e)


### Contributing
Contributions are welcome! Please create an issue or submit a pull request with your improvements.

### License
This project is licensed under the MIT License.

### Contact
For any questions or suggestions, please reach out to any contributors below

## Authors
- *Yufeng Liu*
- *Juan Marulanda*
- *Ishar Ghura*
- *Raphael Onana*
- *Ashwin Srirankan*
