# server.py
from flask import Flask
from main import update_txt_files  # Import the function from your script
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/", methods=['POST'])
def index():
    logger.info(f"Received here!!!!")
    update_txt_files()  # Run the task
    return "Task completed", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)