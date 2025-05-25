import os
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        # Load JSON data
        data_path = os.path.join(os.path.dirname(__file__), "..", "marks.json")
        with open(data_path) as f:
            students = json.load(f)

        # Build a name-to-marks dictionary
        marks_dict = {entry["name"]: entry["marks"] for entry in students}

        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        names = query.get("name", [])

        # Lookup marks
        result = [marks_dict.get(name, None) for name in names]

        # Send JSON response
        self.wfile.write(json.dumps({"marks": result}).encode())
