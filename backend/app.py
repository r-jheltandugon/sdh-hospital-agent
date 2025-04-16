from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Get API key from .env
aiml_api_key = os.getenv("AIML_API_KEY")

if not aiml_api_key:
    raise ValueError("AIML_API_KEY not found in .env file")

# Use AIMLAPI endpoint (OpenAI-compatible)
client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key=aiml_api_key
)

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Something went wrong!"}), 500

@app.route("/")
def index():
    return "Backend is running!"

if __name__ == "__main__":
    app.run(debug=True)
