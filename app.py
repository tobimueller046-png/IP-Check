from flask import Flask, request, render_template
from datetime import datetime, timezone
from pathlib import Path
import csv

app = Flask(__name__)

LOG_FILE = Path("ip_log.csv")


if not LOG_FILE.exists():
    with LOG_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Zeit",
            "IP",
            "Browser"
        ])


@app.route("/")
def home():
    return render_template("index.html")


@app.post("/share")
def share_ip():

    ip = request.remote_addr or "Unbekannt"
    browser = request.headers.get(
        "User-Agent",
        "Unbekannt"
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%d %H:%M:%S UTC")

    with LOG_FILE.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            ip,
            browser
        ])

    return render_template(
        "success.html",
        ip=ip
    )


@app.route("/dashboard")
def dashboard():

    entries = []

    if LOG_FILE.exists():

        with LOG_FILE.open(
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            entries = list(
                csv.DictReader(file)
            )

    entries.reverse()

    return render_template(
        "dashboard.html",
        entries=entries
    )


if __name__ == "__main__":
   app.run(
    host="0.0.0.0",
    port=5000,
    debug=False
)