# 🌍 Travel Recommendation Web App

### 🏆 AI-Powered Destination Finder Using Tweets & Weather Data

This web app **analyzes live Twitter data** to suggest **top travel destinations** based on **sentiment, weather conditions, and popularity**. Users can enter keywords (like "beach" or "Tokyo") and get **real-time travel scores, tweets, and weather updates** for different locations.

---

## 🚀 Features
👉 **Live Twitter Analysis** – Uses **sentiment analysis & NLP** to understand **public opinion** about locations.  
👉 **Weather Integration** – Fetches **real-time weather** for extracted locations.  
👉 **Smart Travel Score** – Assigns **weighted scores** based on **sentiment, weather, and tweet popularity**.  
👉 **Dynamic Frontend** – Built with **React** for a **smooth user experience**.  
👉 **Fast & Scalable Backend** – Uses **Flask & MongoDB** for efficient **data handling**.  
👉 **Caching for Performance** – Reduces API calls with **MongoDB caching**.

---

## 🛠️ Tech Stack
- **Frontend:** React.js, HTML, CSS
- **Backend:** Flask (Python)
- **Database:** MongoDB (for caching)
- **APIs:** Twitter API, OpenWeather API
- **NLP:** SpaCy, TextBlob
- **Containerization:** Docker 

---

## 🔧 Installation & Setup

### **1⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/travel-rec-app.git
cd travel-rec-app
```

### **2⃣ Backend Setup (Flask)**
```bash
cd backend
python -m venv venv   # Create virtual environment
source venv/bin/activate  # Activate environment (Mac/Linux)
venv\Scripts\activate  # (Windows)
pip install -r requirements.txt  # Install dependencies
```

👉 **Set up environment variables in a `.env` file** inside `backend/`:
```ini
TWITTER_BEARER_TOKEN=your_twitter_api_key
WEATHER_API_KEY=your_weather_api_key
MONGO_URI=your_mongodb_uri
```

🛢 **Run the Flask backend:**
```bash
python app.py
```
_(The backend runs on `http://127.0.0.1:5000`)_

---

### **3⃣ Frontend Setup (React)**
```bash
cd ../frontend
npm install  # Install dependencies
npm start    # Start React app
```
_(The frontend runs on `http://localhost:3000`)_

---

## 🔥 How It Works

1️⃣ **User enters a keyword** (e.g., "Paris", "beach")  
2️⃣ The app **fetches recent tweets** mentioning the keyword.  
3️⃣ **Natural Language Processing (NLP)** extracts **locations & sentiment**.  
4️⃣ The app **fetches weather** for each location.  
5️⃣ A **travel score** is assigned based on **sentiment, weather, & tweet popularity**.  
6️⃣ The app **displays ranked travel recommendations** with tweets & weather info.  

---

## 🌿 API Endpoints (Flask)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Check if API is running |
| `GET` | `/analyze-tweets?query=beach` | Fetch tweets, weather & travel scores |
| `GET` | `/add-sample` | Insert test data into MongoDB |
| `GET` | `/get-sample` | Fetch test data from MongoDB |

---

## 📌 Future Improvements
👉 **More Data Sources** (e.g., Google Reviews, TripAdvisor)  
👉 **Interactive Maps** to visualize **popular locations**  
👉 **User Ratings & Reviews** for travel locations  
👉 **Dark Mode & Mobile UI Enhancements**  

---

## 🤝 Contributing
1. **Fork the repo**
2. **Create a new branch** (`git checkout -b feature-name`)
3. **Commit your changes** (`git commit -m "Added feature X"`)
4. **Push to GitHub** (`git push origin feature-name`)
5. **Submit a Pull Request**

---

## ⚡ Author
**👩‍💻 Ridhima Morampudi**  
🌟 Follow me on [GitHub](https://github.com/ridhimamorampudi)  
📧 Contact: `rmorampudi@g.ucla.edu`

---

## 🐝 License
This project is licensed under the **MIT License**.

---

