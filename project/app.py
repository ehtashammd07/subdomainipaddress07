from flask import Flask, jsonify, request, render_template
import requests
from flask_cors import CORS  # Import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the app
CORS(app)  # This will allow all domains to access the backend by default

# You can use any IP lookup service here (e.g., ip-api, ipinfo, or ipstack)
API_URL = "http://extreme-ip-lookup.com/json/"  # This is the URL for the free IP API service.

@app.route('/')
def home():
    return render_template('index.html')  # Serve the index.html file from templates folder

@app.route('/search_ip', methods=['GET'])
def search_ip():
    query = request.args.get('query')  # Get the query parameter from the URL.

    if not query:
        return jsonify({"error": "No query parameter provided"}), 400  # If no query is provided, return an error.

    # Now, you send the query to the IP API to get the details
    response = requests.get(f'{API_URL}{query}')  # This fetches IP details from the IP API service.

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch IP data"}), 500  # If there was an error with the API request, return a 500 error.
    
    data = response.json()  # Parse the response as JSON.

    if data.get('status') == 'fail':  # If the query was not valid.
        return jsonify({"error": "Invalid IP address or query"}), 400

    # Extract the required data and return it in the desired format
    return jsonify({
        'ip': data.get('query'),
        'city': data.get('city', 'N/A'),
        'region': data.get('region', 'N/A'),
        'country': data.get('country', 'N/A'),
        'postal_code': data.get('zip', 'N/A'),
        'isp': data.get('isp', 'N/A'),
        'asn': data.get('as', 'N/A')
    })

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
