import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN") 
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
EMERGENCY_CONTACT = os.getenv("EMERGENCY_CONTACT")

# AI Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Validation
required_vars = [
    "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", 
    "TWILIO_FROM_NUMBER", "EMERGENCY_CONTACT", "GROQ_API_KEY"
]

for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")
