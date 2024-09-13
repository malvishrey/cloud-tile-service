# server.py
from flask import Flask, request, jsonify
from main import generate_tile_service  # Import the function from your script
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/", methods=['POST'])
def index():
    try:
        # Extract data from the request
        # data = request.json
        # date = data.get('date')
        # confidence = data.get('confidence')
        # geojson = data.get('geojson')
        # asu_snow = data.get('asu_snow')

        # # Log received data
        # logger.info(f"Received data: date={date}, confidence={confidence}, geojson={geojson}, asu_snow={asu_snow}")

        # Call your task or function with these arguments
        msg = generate_tile_service("", "", "", "")

        return jsonify({"message": msg}), 200

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": "Failed to process request"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)