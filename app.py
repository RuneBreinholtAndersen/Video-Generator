from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_video():
    data = request.json
    api_key = os.getenv("GEMINI_API_KEY")
    prompt = data.get("prompt")
    image = data.get("image")  # Dict med 'mime_type' og 'data'

    if not api_key or not prompt:
        return jsonify({"error": "Missing API key or prompt"}), 400

    payload = {
        "prompt": prompt,
        "duration": "8s",
        "aspect_ratio": "16:9",
        "output_resolution": "720p"
    }

    # Hvis billede er sendt med
    if image and "data" in image and "mime_type" in image:
        payload["image"] = {
            "mime_type": image["mime_type"],
            "data": image["data"]
        }

    # Kald til Gemini Veo API
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/veo-2.0-generate-001:generateVideo?key=" + api_key,
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code
