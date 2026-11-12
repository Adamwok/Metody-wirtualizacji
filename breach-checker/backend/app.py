import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])

def load_hashes(path="/app/data/leaked-sha1.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}

KNOWN_HASHES = load_hashes()
print(f"Wczytano {len(KNOWN_HASHES)} hashy z /app/data/leaked-sha1.txt")

@app.post("/check")
def check():
    data = request.get_json(silent=True) or {}
    h = data.get("hash")
    if not h or not isinstance(h, str):
        return jsonify({"error": "Brak pola hash"}), 400

    h = h.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{40}", h):
        return jsonify({"error": "Nieprawidlowy format SHA-1"}), 400

    print(f"Sprawdzam skrot: {h[:5]}...")
    found = h in KNOWN_HASHES
    return jsonify({"found": found})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)