# -*- coding: utf-8 -*-
import sys
import io

# Set default encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


import mysql.connector
from datetime import datetime

import mysql.connector

class FoodQuestDB:
    def __init__(self, dbname, user, host, port, password):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=dbname,
                port=port
            )
            self.cur = self.connection.cursor()
            print(" Successfully connected to MySQL!")
        except mysql.connector.Error as err:
            print(f" Database connection failed: {err}")
            self.connection = None  # Avoid breaking the app if connection fails


    def __del__(self):
        self.cur.close()
        self.connection.close()

    def execute_query(self, query, params=None, fetch_one=False):
        try:
            self.cur.execute(query, params or ())
            if query.strip().upper().startswith("SELECT"):
                return self.cur.fetchone() if fetch_one else self.cur.fetchall()
            else:
                self.connection.commit()
                return self.cur.rowcount
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return None

    def get_user_points_by_food(self, user_id):
        query = """
            SELECT f.food_name, p.points_awarded
            FROM points p
            JOIN foods f ON p.food_id = f.food_id
            WHERE p.user_id = %s
        """
        return self.execute_query(query, (user_id,))

    def get_users_ordered_by_points(self):
        query = """
        SELECT u.user_id, u.username, COALESCE(SUM(p.points_awarded), 0) AS total_points
        FROM users u
        LEFT JOIN points p ON u.user_id = p.user_id
        GROUP BY u.user_id, u.username
        ORDER BY total_points DESC;
        """
        result = self.execute_query(query)

        # Debugging
        print(f"SQL Query Result: {result}")  

        if result is None:
            print("⚠️ Query returned None. Possible SQL error!")
            return []

        return [{"id": user[0], "username": user[1], "points": user[2]} for user in result]

        
    def get_user_rank(self, user_id):
        query = """
            SET @rank = 0;
            SELECT user_id, username, total_points, @rank := @rank + 1 AS rank
            FROM (
                SELECT u.user_id, u.username, IFNULL(SUM(p.points_awarded), 0) AS total_points
                FROM users u
                LEFT JOIN points p ON u.user_id = p.user_id
                GROUP BY u.user_id, u.username
                ORDER BY total_points DESC
            ) ranked_users
            WHERE user_id = %s;
        """
        result = self.execute_query(query, (user_id,), fetch_one=True)
        return result[0] if result else None

    def food_submission_times_of_user(self, user_id):
        query = """
            SELECT f.food_name, p.time_submitted, p.points_awarded
            FROM points p
            JOIN foods f ON p.food_id = f.food_id
            WHERE p.user_id = %s
            ORDER BY time_submitted DESC;
        """
        result = self.execute_query(query, (user_id,))
        if result:
            return [
                (food_name, time_submitted.strftime("%Y-%m-%d %H:%M:%S"), points_awarded)
                for food_name, time_submitted, points_awarded in result
            ]
        return None
    
    def get_all_users(self):
        query = "SELECT * FROM users NATURAL JOIN points;"
        return self.execute_query(query)

    def get_username(self, user_id):
        query = "SELECT username FROM users WHERE user_id = %s"
        result = self.execute_query(query, (user_id,), fetch_one=True)
        return result[0] if result else None

    def insert_food(self, food_name, points, expiry_date, user_id):
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert into foods table
        food_query = "INSERT INTO foods (food_name, expiry) VALUES (%s, %s)"
        self.execute_query(food_query, (food_name, expiry_date))

        # Get last inserted food_id
        self.cur.execute("SELECT LAST_INSERT_ID()")
        food_id = self.cur.fetchone()[0]

        # Insert into points table
        points_query = """
            INSERT INTO points (food_id, user_id, time_submitted, points_awarded)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(points_query, (food_id, user_id, time_now, points))

# Usage example:
if __name__ == "__main__":
    MYSQL_PASS = "your_mysql_password"
    db = FoodQuestDB("FoodQuest", "your_mysql_user", "localhost", 3306, MYSQL_PASS)

    # Example usage of methods
    user_id = 1
    print(db.get_user_points_by_food(user_id))
    print(db.get_users_ordered_by_points())
    print(db.get_user_rank(user_id))
    print(db.food_submission_times_of_user(user_id))
    print(db.get_username(user_id))
