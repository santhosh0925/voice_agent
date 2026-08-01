import os
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
from livekit.api import AccessToken, VideoGrants


app = Flask(__name__)
CORS(app, resources={r"/*": {"origin": "*"}})


def generate_room():
    return "room-" + str(uuid.uuid4())[:8]


@app.route("/api/health")
@app.route("/health")
def health():
    return jsonify({"ok": True})


@app.route("/api/config")
@app.route("/config")
def config():
    livekit_url = os.environ.get("LIVEKIT_URL")
    if not livekit_url:
        return jsonify({"error": "Missing LIVEKIT_URL"}), 500
    return jsonify({"livekitUrl": livekit_url})


@app.route("/api/getToken")
@app.route("/getToken")
def get_token():
    name = request.args.get("name", "guest")
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
