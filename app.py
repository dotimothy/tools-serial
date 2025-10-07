# app.py
import sys
import subprocess
import os
import argparse
import webbrowser

# --- Dependency Installation ---
# Map the pip install name to the name used for importing
required_packages = {
    'Flask': 'flask',
    'pyopenssl': 'OpenSSL'
}

print("Checking for required packages...")
for install_name, import_name in required_packages.items():
    try:
        # Try to import the package by its import name
        __import__(import_name)
    except ImportError:
        # If import fails, install the package using its pip install name
        print(f"'{install_name}' not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {install_name}. Please install it manually.", file=sys.stderr)
            sys.exit(1)

print("All packages are installed. Starting the Flask app...")
# --- End of Installation ---

from flask import Flask, send_from_directory, abort

# --- Main Application ---
SERVE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME = os.path.basename(__file__)

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(SERVE_DIR, 'index.html')

@app.route('/<path:path>')
def serve_files(path):
    if path == SCRIPT_NAME:
        abort(404)
    return send_from_directory(SERVE_DIR, path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a Flask file server with ad-hoc HTTPS.")
    parser.add_argument('--host', default='127.0.0.1', help='The host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='The port to listen on (default: 5000)')

    args = parser.parse_args()

    # --- Auto-launch Browser ---
    URL = f"https://{args.host}:{args.port}"
    print(f"Starting server on {URL}")
    
    try:
        webbrowser.open_new_tab(URL)
        print("Opening browser...")
    except webbrowser.Error as e:
        print(f"Could not open browser: {e}")
        print("Please open the URL manually in your browser.")
    # --- End of Auto-launch ---

    app.run(host=args.host, port=args.port, ssl_context='adhoc')

