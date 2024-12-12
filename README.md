# X (Twitter) Automation API

## 📝 Description
This Flask-based web application allows users to post tweets immediately or schedule tweets for future posting using the X (Twitter) API. The application provides a simple web interface for managing social media posts.

## ✨ Features
- Instant tweet posting
- Tweet scheduling
- View scheduled posts
- Web-based user interface

## 🛠 Prerequisites
- Python 3.8+
- Flask
- Tweepy
- APScheduler

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone git@github.com:jk08y/x-api.git
cd x-api
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Credentials
Create a `.env` file or update the credentials directly in `app.py`:
- `API_KEY`: X Developer API Key
- `API_SECRET`: X Developer API Secret
- `ACCESS_TOKEN`: X Access Token
- `ACCESS_SECRET`: X Access Token Secret
- `BEARER_TOKEN`: X Bearer Token

## 🔧 Running the Application
```bash
python app.py
```
Navigate to `http://localhost:5000` in your web browser.

## 📋 Project Structure
- `app.py`: Main Flask application
- `scheduler.py`: Handles tweet scheduling logic
- `templates/`: HTML template files
  - `home.html`: Main page for instant posting
  - `schedule.html`: Page for scheduling tweets
  - `posts.html`: View scheduled posts

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Important Notes
- Ensure you have valid X Developer credentials
- Keep your API keys and tokens confidential
- Comply with X's Developer Terms of Service

## 📄 License
[MIT License]

## 🐛 Issues
Report issues at: https://github.com/jk08y/x-api/issues
