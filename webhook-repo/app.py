from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://rishabhrthr001:Bv7Bsr4g7Nbnc3a2@cluster0.qars1vk.mongodb.net/")
db = client["webhookDB"]
events = db["events"]

@app.route('/webhook', methods=['POST'])
def webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    print("Event Type:", event)
    print("Payload:", payload)

    if event == 'push':
        try:
            author = payload['pusher']['name']
            branch = payload['ref'].split('/')[-1]
            timestamp = payload['head_commit']['timestamp']
            print("Saving PUSH to MongoDB...")
            events.insert_one({
                "type": "push",
                "author": author,
                "to_branch": branch,
                "timestamp": timestamp
            })
        except Exception as e:
            print("Push insert error:", e)

    elif event == 'pull_request':
        try:
            pr = payload['pull_request']
            author = pr['user']['login']
            from_branch = pr['head']['ref']
            to_branch = pr['base']['ref']
            merged = pr['merged']
            timestamp = pr['merged_at'] if merged else pr['created_at']
            print("Saving PR/MERGE to MongoDB...")

            events.insert_one({
                "type": "merge" if merged else "pull_request",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            })
        except Exception as e:
            print("PR insert error:", e)

    return jsonify({"status": "received"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    result = events.find().sort("timestamp", -1).limit(10)
    formatted = []
    for r in result:
        if r["type"] == "push":
            formatted.append(f'{r["author"]} pushed to {r["to_branch"]} on {format_time(r["timestamp"])}')
        elif r["type"] == "pull_request":
            formatted.append(f'{r["author"]} submitted a pull request from {r["from_branch"]} to {r["to_branch"]} on {format_time(r["timestamp"])}')
        elif r["type"] == "merge":
            formatted.append(f'{r["author"]} merged branch {r["from_branch"]} to {r["to_branch"]} on {format_time(r["timestamp"])}')
    return jsonify(formatted)

def format_time(ts):
    try:
        utc_time = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        utc_time = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z") 
        utc_time = utc_time.astimezone(pytz.utc)

    utc_time = utc_time.replace(tzinfo=pytz.utc)
    ist_time = utc_time.astimezone(pytz.timezone("Asia/Kolkata"))
    return ist_time.strftime("%d %B %Y - %I:%M %p IST")

if __name__ == "__main__":
    app.run(debug=True)
