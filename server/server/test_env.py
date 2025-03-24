from dotenv import load_dotenv
import os

load_dotenv()

print("Database Name:", os.getenv("DATABASE_NAME"))
print("Database Password:", os.getenv("PASSWORD"))
