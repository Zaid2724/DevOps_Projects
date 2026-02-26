from flask import Flask, request
import subprocess
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if data:
        for alert in data.get("alerts", []):
            status = alert.get("status")
            alertname = alert.get("labels", {}).get("alertname")

            if alertname == "NginxDown" and status == "firing":
                print("Nginx is down. Restarting...")
                subprocess.run(
                    ["sudo", "systemctl", "restart", "nginx"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return "Nginx Restarted", 200

    return "No Action Taken", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)