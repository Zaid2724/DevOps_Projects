🚀 Self-Healing Infrastructure with Prometheus & Alertmanager
📌 Overview

This project demonstrates a self-healing monitoring system built using:

Prometheus – Monitoring & alerting engine

Node Exporter – System metrics collection

Alertmanager – Alert routing

Flask (Python Webhook) – Automated recovery trigger

systemd – Service management

The system automatically detects when Nginx goes down and restarts it without manual intervention.

🏗 Architecture
Node Exporter → Prometheus → Alertmanager → Flask Webhook → systemctl restart nginx
<img width="1536" height="1024" alt="Self_healing_infra" src="https://github.com/user-attachments/assets/4bdb8237-debb-4325-8768-0f19a0bae1e8" />


🔄 Flow

Node Exporter exposes system metrics.

Prometheus scrapes metrics and evaluates alert rules.

If Nginx is down, Prometheus fires an alert.

Alertmanager sends the alert to a webhook.

The Flask webhook automatically runs:

sudo systemctl restart nginx

Nginx is restored automatically.

�� Project Structure
self-healing/
│
├── webhook.py
├── venv/
├── alert.rules.yml
├── prometheus.yml
└── README.md
⚙️ Setup Guide
1️⃣ Install Dependencies
sudo apt update
sudo apt install nginx python3 python3-venv -y
2️⃣ Install Node Exporter

Download from:
https://prometheus.io/download/

Run Node Exporter:

./node_exporter
3️⃣ Install Prometheus

Download from:
https://prometheus.io/download/

Configure prometheus.yml:

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
4️⃣ Create Alert Rule

alert.rules.yml

groups:
- name: nginx-alerts
  rules:
  - alert: NginxDown
    expr: up{job="node"} == 0
    for: 30s
    labels:
      severity: critical
    annotations:
      summary: "Nginx is down"
5️⃣ Setup Flask Webhook

Create virtual environment:

python3 -m venv venv
source venv/bin/activate
pip install flask

webhook.py

from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Nginx is down. Restarting...")
    subprocess.run(["sudo", "systemctl", "restart", "nginx"])
    return "Restarted", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
6️⃣ Allow Passwordless Restart

Edit sudoers:

sudo visudo -f /etc/sudoers.d/nginx-restart

Add:

ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl restart nginx
7️⃣ Configure Alertmanager Webhook

In alertmanager.yml:

route:
  receiver: ansible-webhook

receivers:
- name: ansible-webhook
  webhook_configs:
  - url: "http://localhost:5001/webhook"
8️⃣ Run Webhook as systemd Service

Create:

sudo nano /etc/systemd/system/self-healing.service

Add:

[Unit]
Description=Self Healing Webhook Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/self-healing
ExecStart=/home/ubuntu/self-healing/venv/bin/python3 /home/ubuntu/self-healing/webhook.py
Restart=always

[Install]
WantedBy=multi-user.target

Enable:

sudo systemctl daemon-reload
sudo systemctl enable self-healing
sudo systemctl start self-healing
🧪 Testing the Automation

Stop Nginx:

sudo systemctl stop nginx

Within seconds:

Prometheus detects failure

Alertmanager sends webhook

Webhook restarts Nginx automatically

Verify:

sudo systemctl status nginx

You should see:

Active: active (running)
