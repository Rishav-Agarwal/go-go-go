import json
import os
import time
from threading import Thread
from flask import Flask, redirect, abort

app = Flask(__name__)

# Global variable to store mappings
go_links = {}
mappings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mappings.json")
last_modified = 0

def load_mappings():
    """Load mappings from the JSON file"""
    global go_links, last_modified
    try:
        # Check if file exists and get its modification time
        if os.path.exists(mappings_file):
            current_modified = os.path.getmtime(mappings_file)
            
            # Only reload if file has been modified
            if current_modified > last_modified:
                with open(mappings_file, 'r') as f:
                    go_links = json.load(f)
                last_modified = current_modified
                print(f"Loaded {len(go_links)} mappings from {mappings_file}")
        else:
            print(f"Warning: {mappings_file} not found. Using empty mappings.")
            go_links = {}
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading mappings: {e}")
        # Keep existing mappings if there's an error

def watch_mappings_file():
    """Background thread to watch for file changes"""
    while True:
        load_mappings()
        time.sleep(60)  # Check every minute

@app.route("/<name>")
def go_link(name):
    # Reload mappings on each request to ensure we have the latest
    load_mappings()
    
    url = go_links.get(name)
    if url:
        return redirect(url)
    else:
        return abort(404, description="Go link not found")

@app.route("/")
def index():
    # Reload mappings to show current state
    load_mappings()
    
    html = "<h1>Available Go Links</h1><ul>"
    for name, url in go_links.items():
        html += f'<li><a href="/go/{name}">go/{name}</a> → {url}</li>'
    html += "</ul>"
    html += f"<p>Mappings loaded from: {mappings_file}</p>"
    html += "<p>Edit the mappings.json file to update links in real-time!</p>"
    return html

if __name__ == "__main__":
    # Load initial mappings
    load_mappings()
    
    # Start file watcher in background thread
    watcher_thread = Thread(target=watch_mappings_file, daemon=True)
    watcher_thread.start()
    
    print(f"Starting server with {len(go_links)} mappings loaded from {mappings_file}")
    print("Edit mappings.json to update links in real-time!")
    app.run(host="127.0.0.1", port=9191)

