import os

import requests
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:5000")


@app.get("/")
def index():
    resp = requests.get(f"{BACKEND_URL}/messages", timeout=5)
    messages = resp.json() if resp.ok else []
    return render_template("index.html", messages=messages)


def client_ip() -> str:
    # X-Forwarded-For é preenchido por proxies/load balancers; o primeiro IP é o do cliente
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "desconhecido"


@app.post("/post")
def post():
    name = request.form.get("name", "").strip()
    text = request.form.get("text", "").strip()
    if name and text:
        requests.post(
            f"{BACKEND_URL}/messages",
            json={"name": name, "text": text, "ip_client": client_ip()},
            timeout=5,
        )
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
