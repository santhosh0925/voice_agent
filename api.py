import os
import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from livekit.api import AccessToken, VideoGrants

load_dotenv()

def generate_room():
    return "room-"+ str(uuid.uuid4())[:8]

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*":{"origin":"*"}})

    @app.route("/api/health")
    @app.route("/health")
    def health():
        return jsonify({"ok": True})

    @app.route("/api/config")
    @app.route("/config")
    def config():
        livekit_url = os.environ.get("LIVEKIT_URL")
        if not livekit_url:
            return jsonify({
                "error": "Missing LIVEKIT_URL"
            }), 500
        return jsonify({"livekitUrl": livekit_url})

    @app.route("/api/getToken")
    @app.route("/getToken")
    def get_token():
        name = request.args.get("name","guest")
        room = request.args.get("room", generate_room())
        api_key = os.environ.get("LIVEKIT_API_KEY")
        api_secret = os.environ.get("LIVEKIT_API_SECRET")
        if not api_key or not api_secret:
            return jsonify({
                "error": "Missing LIVEKIT_API_KEY or LIVEKIT_API_SECRET"
            }), 500

        grants = VideoGrants(room_join=True, room=room)
        token = AccessToken(api_key, api_secret).with_identity(name).with_grants(grants)
        return jsonify({
            "token": token.to_jwt(),
            "room": room,
            "identity": name
        })

    return app

if __name__ == "__main__":
    # Run locally for development
    create_app().run(host="0.0.0.0", port=5001, debug=False)
