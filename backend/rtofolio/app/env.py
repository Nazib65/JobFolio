import os
from dotenv import load_dotenv

# 1. Load the .env file immediately
load_dotenv() 

# 2. Now os.getenv will find the value
DATABASE_URL = os.getenv("DATABASE_URL")

# Debug print to verify it works (remove this later)
print(f"Loaded DATABASE_URL: {DATABASE_URL}")