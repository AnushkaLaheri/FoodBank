import mysql.connector

MYSQL_PASS = "Anushka@01"  # Change with your MySQL password

# Establishing the MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="anushka",
    password=MYSQL_PASS,
    database="FoodQuest"
)

# Creating a cursor object to interact with the database
cur = connection.cursor()
if connection.is_connected():
    print("Connected to MySQL successfully!")

def get_user_points_by_food(user_id):
    try:
        cur.execute(
            """
            SELECT f.food_name, p.points_awarded
            FROM points p
            JOIN foods f ON p.food_id = f.food_id
            WHERE p.user_id = %s
            """,
            (user_id,)
        )

        result = cur.fetchall()

        if result:
            return result
        else:
            return None

    except mysql.connector.Error as err:
        print("Error retrieving user's points: ", err)
        return None


def get_users_ordered_by_points():
    try:
        cur.execute(
            """
            SELECT u.user_id, u.username, COALESCE(SUM(p.points_awarded), 0) AS total_points
            FROM users u
            LEFT JOIN points p ON u.user_id = p.user_id
            GROUP BY u.user_id, u.username
            ORDER BY total_points DESC;
            """
        )

        result = cur.fetchall()

        formatted_users = [
            {"id": user[0], "username": user[1], "points": user[2]} for user in result
        ]
        return formatted_users

    except mysql.connector.Error as err:
        print("Error retrieving all the users' points: ", err)
        return None


def get_user_rank(user_id):
    try:
        cur.execute(
            """
            SELECT rank
            FROM (
                SELECT u.user_id, u.username, COALESCE(SUM(p.points_awarded), 0) AS total_points,
                RANK() OVER (ORDER BY COALESCE(SUM(p.points_awarded), 0) DESC) AS rank
                FROM users u
                LEFT JOIN points p ON u.user_id = p.user_id
                GROUP BY u.user_id, u.username
            ) AS ranked_users
            WHERE user_id=%s
            """,
            (user_id,)
        )

        result = cur.fetchall()

        if result:
            return result
        else:
            return None

    except mysql.connector.Error as err:
        print("Error retrieving user's rank: ", err)
        return None


def food_submission_times_of_user(user_id):
    try:
        cur.execute(
            """
            SELECT f.food_name, p.time_submitted, p.points_awarded
            FROM points p
            JOIN foods f ON p.food_id = f.food_id
            WHERE p.user_id = %s
            """,
            (user_id,)
        )

        result = cur.fetchall()

        time_formatted = [
            (food_name, time_submitted.strftime("%Y-%m-%d %H:%M:%S"), points_awarded)
            for food_name, time_submitted, points_awarded in result
        ]

        return time_formatted if time_formatted else None

    except mysql.connector.Error as err:
        print("Error retrieving user's foods' sub times: ", err)
        return None


def get_username(user_id):
    try:
        cur.execute(
            """
            SELECT u.username
            FROM users u
            WHERE u.user_id = %s
            """,
            (user_id,)
        )

        result = cur.fetchall()

        if result:
            return result
        else:
            return None

    except mysql.connector.Error as err:
        print("Error retrieving user's foods' sub times: ", err)
        return None

# Don't forget to close the cursor and connection when done
cur.close()
connection.close()
