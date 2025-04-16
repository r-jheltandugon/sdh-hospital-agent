# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables (like OpenAI API key)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend access
CORS(app)

# OpenAI API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Welcome to the AI Chatbot backend!"

@app.route("/chat", methods=["POST"])
def chat():
    # Get the user's message from the frontend
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Call OpenAI API with the user's message
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or GPT-4 if you prefer
        messages=[{"role": "user", "content": user_message}],
    )

    # Extract AI's reply from the OpenAI response
    ai_reply = response.choices[0].message.content.strip()

    # Return the AI's response to the frontend
    return jsonify({"reply": ai_reply})


if __name__ == "__main__":
    app.run(debug=True)
