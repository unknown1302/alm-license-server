from flask import Flask, request, jsonify

app = Flask(__name__)

# Example: In-memory license "database"
licenses = {
    "HWID1|AppID1": {"key": "SAMPLEKEY|20260101", "expiry": "20260101", "status": "active"},
}

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    hwid = data.get('hwid')
    appid = data.get('appid')
    key = data.get('key')
    today = data.get('today')

    lookup = f"{hwid}|{appid}"
    record = licenses.get(lookup)

    if not record or record["key"] != key:
        return jsonify({"status": "invalid"}), 200
    elif record["status"] != "active":
        return jsonify({"status": record["status"]}), 200
    elif record["expiry"] < today:
        return jsonify({"status": "expired"}), 200
    else:
        return jsonify({"status": "valid", "expiry": record["expiry"]}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
