# 🚀 Zoom Chat Spam Detection Bot

## 📌 Overview
A **real-time spam detection system** for Zoom chat rooms using **Python, FastAPI, OpenAI, and React.js**. This tool **automatically detects spam messages** and provides a **dashboard** for monitoring chat activity.

## 🔧 Features
✅ **Real-time Spam Detection** – Detect spam using regex and AI (OpenAI API).  
✅ **Zoom API Integration** – Fetch messages from Zoom chat automatically.  
✅ **Live Monitoring Dashboard** – View spam trends with a React.js frontend.  
✅ **Error Logging & Notifications** – Logs spam attempts & sends alerts (Discord, email, or Telegram).  
✅ **Admin Panel** – Configure spam rules & manage flagged messages.  

## 📁 Project Structure
```bash
📂 zoom-spam-detector
├── 📂 backend  # FastAPI Server
│   ├── main.py  # API Routes
│   ├── spam_filter.py  # Spam detection logic
│   ├── zoom_api.py  # Zoom API Integration
│   ├── database.py  # Stores logs & flagged messages
│   └── .env  # API keys & secrets (DO NOT SHARE)
│
├── 📂 frontend  # React.js Dashboard
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── App.js
│
├── 📂 logs  # Stores error & spam logs
├── README.md  # Project Documentation
└── .gitignore  # Ignore sensitive files
```

## ⚙️ Installation & Setup
### **1️⃣ Backend Setup (Python/FastAPI)**
```sh
# Clone the repo
git clone https://github.com/yourusername/zoom-spam-detector.git
cd zoom-spam-detector/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload
```
API will be available at: `http://localhost:8000`

### **2️⃣ Frontend Setup (React.js)**
```sh
cd ../frontend

# Install dependencies
npm install

# Start the React dashboard
npm start
```
Frontend will be available at: `http://localhost:3000`

## 🔑 Environment Variables
Create a `.env` file in `backend/` and add:
```ini
ZOOM_API_KEY=your_zoom_api_key
ZOOM_API_SECRET=your_zoom_api_secret
OPENAI_API_KEY=your_openai_api_key
```

## 🚀 Deployment
- **Backend:** Deploy using **AWS, Render, or DigitalOcean**.
- **Frontend:** Deploy on **Vercel, Netlify, or Firebase Hosting**.
- **Database:** Use **PostgreSQL or MongoDB** for scalability.

## 📜 License
MIT License - Use freely but give credit! 😊

## 🌟 Contributing
Feel free to submit PRs & suggestions. Let's build a **spam-free chat experience** together!

## 📬 Contact
For any questions, reach out via [GitHub Issues](https://github.com/yourusername/zoom-spam-detector/issues)!
