# 🔔 webhook-repo

This is a full-stack application that receives GitHub webhook events (Push, Pull Request, and Merge) and displays them in a React frontend, powered by a Flask backend and MongoDB Atlas for storage.

It works in tandem with [`action-repo`](https://github.com/rishabhrthr001/action-repo), which triggers the events.

---

## 📌 Features

- ✅ Listens to GitHub webhook events:
  - Push
  - Pull Request
  - Merge (via PR)
- ✅ Stores event data in MongoDB Atlas
- ✅ Displays the latest 10 events in a beautiful UI
- ✅ Auto-refreshes every 15 seconds
- ✅ Timestamps displayed in **IST**

---

## 🛠️ Tech Stack

| Layer       | Tech            |
|-------------|------------------|
| Frontend    | React (JS)       |
| Backend     | Flask + Flask-CORS |
| Database    | MongoDB Atlas    |
| Webhooks    | GitHub → Flask   |
| Styling     | CSS (custom)     |

---

## 🖥️ UI Screenshot


![GitHub Events UI](./assets/screenshot.png)

---

## 🔗 How it Works

1. A webhook is added in `action-repo` GitHub settings
2. On every push / PR / merge, GitHub sends a JSON payload to `/webhook`
3. Flask parses the event and stores it in MongoDB
4. React app fetches `/events` every 15s and displays formatted updates

---

## 📂 Project Structure


---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/rishabhrthr001/webhook-repo.git
cd webhook-repo


2. Start Flask Backend

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py


3. Start React Frontend

cd frontend
npm install
npm start



🔄 Webhook Setup
Start backend locally (localhost:5000)

Use ngrok to expose your server:

ngrok http 5000



📦 Sample Event Formats
Push:
"Rishabh pushed to main on 03 July 2025 - 06:00 PM IST"

Pull Request:
"Rishabh submitted a pull request from dev to main on ..."

Merge:
"Rishabh merged branch feature-x to main on ..."