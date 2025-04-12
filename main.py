from flask import Flask, render_template, jsonify, request
import requests
from flask_cors import CORS
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan")
def scan_domain():

    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "Domain parameter is required"}), 400
    
    try:
        if not domain.startswith(("http://", "https://")):
            domain = f"https://{domain}"
        
        print(f"Received scan request for: {domain}")  # Добавьте это

        result = urlparse(domain)
        if not all([result.scheme, result.netloc]):
            return jsonify({"error":"no corect url format"}), 400
        response = requests.get(
            domain,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
        )
        return jsonify({
            "headers": dict(response.headers),
            "status_code": response.status_code
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to scan domain: {str(e)}",
            "domain": f"{domain}"
            }), 500

if __name__ == "__main__":
    app.run(debug=True)