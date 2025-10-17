from flask import Flask, request, jsonify, render_template
import requests
import os

# Flask initialisering (templates mappe er eksplicit sat)
app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    """Vis forsiden med uploadfeltet."""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_video():
    """Kalder Gemini Veo API for at generere video baseret på prompt og evt. billede."""
    data = request.json
    api_key = os.getenv("GEMINI_API_KEY")

    # Debug-linje for at se om API-nøglen bliver læst i Render
    print("🔍 API KEY loaded?", bool(api_key))

    # Hent prompt og evt. billede
    prompt = data.get("prompt")
    image = data.get("image")  # Dict med 'mime_type' og 'data'

    if not api_key or not prompt:
        return jsonify({"error": "Missing API key or prompt"}), 400

    # Opsæt payload til Gemini Veo API
    payload = {
        "prompt": prompt,
        "duration": "8s",
        "aspect_ratio": "16:9",
        "output_resolution": "720p"
    }

    # Tilføj billede hvis det er sendt med
    if image and "data" in image and "mime_type" in image:
        payload["image"] = {
            "mime_type": image["mime_type"],
            "data": image["data"]
        }

    # Kald Gemini API
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/veo-002:generateVideo?key={api_key}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.ok:
            print("✅ Video generation succeeded")
            return jsonify(response.json())
        else:
            print("❌ API returned error:", response.text)
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        print("🔥 Internal server error:", str(e))
        return jsonify({"error": str(e)}), 500


# Lokal kørsel (bruges kun hvis du tester lokalt)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
