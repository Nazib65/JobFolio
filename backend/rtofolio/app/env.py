import os
from dotenv import load_dotenv

# 1. Load the .env file immediately
load_dotenv(".env.local")

# 2. Now os.getenv will find the value
DATABASE_URL = os.getenv("DATABASE_URL")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Debug print to verify it works (remove this later)
# print(f"Loaded DATABASE_URL: {DATABASE_URL}")