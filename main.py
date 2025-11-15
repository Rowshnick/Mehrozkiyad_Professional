from flask import Flask
import threading
from bot import run_bot

app = Flask(__name__)

@app.route("/")
def home():
    return "Mehrozkiyad Telegram Bot is running on Render!"

# Run Telegram bot in background thread
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
