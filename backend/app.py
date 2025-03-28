import os
import requests
import time
import spacy #NLP for named entity recognition
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from textblob import TextBlob #NLP sentiment
from datetime import datetime, timedelta


#Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

#Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

#Twitter bearer token from .env
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

MONGO_URI = "mongodb+srv://ridhimamorampudi:I1J4bBxxogfUu5tz@rmcluster.pnjszgb.mongodb.net/?retryWrites=true&w=majority&appName=RMCluster"
client = MongoClient(MONGO_URI)
db = client["travel-app"]
collection = db["test-data"]
tweets_collection = db["tweets"]

#function to extract locations using NER
def extract_locations(text):
    doc = nlp(text)
    #GPE is geo political entity
    locations = [
        ent.text for ent in doc.ents 
        if ent.label_ == "GPE" and not ent.text.startswith("@") and len(ent.text) > 1
    ]
    return locations

def get_weather(location):
    if not WEATHER_API_KEY:
        return {"error": "Missing WEATHER_API_KEY"}

    # Print location being searched (for debugging)
    print(f"Fetching weather for: {location}")

    # Convert multi-word locations like "Cape Town" → "Cape Town,ZA"
    location_query = location.replace(" ", "%20")  # Ensure spaces don't break the request
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location_query}&units=metric&appid={WEATHER_API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Weather API failed for {location}: {response.status_code} - {response.text}")
        return {"error": f"Weather API error: {response.status_code}"}

    try:
        data = response.json()
        if "main" not in data or "weather" not in data:
            print(f"Unexpected weather data format for {location}: {data}")
            return {"error": "Invalid weather API response"}
        
        return {
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
    except KeyError as e:
        print(f"Unexpected weather data format for {location}: {data}")
        return {"error": f"Unexpected weather API response: {e}"}



#function to fetch tweets
def get_tweets(query, count=10):
    #Check if mongoDB if we have recent tweets (within 10 min)
    recent_tweets = tweets_collection.find_one({"query": query})

    if recent_tweets:
        # Convert stored timestamp (float) to datetime for comparison
        cached_time = recent_tweets["timestamp"]
        if isinstance(cached_time, float):
            cached_time = datetime.utcfromtimestamp(cached_time)  # FIXED: Convert float timestamp to datetime

        # If tweets are recent (less than 10 min old), return them
        if datetime.utcnow() - cached_time < timedelta(minutes=10):
            return recent_tweets["tweets"]


    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results={count}&tweet.fields=text"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Twitter API error: {response.status_code}"}
    
    tweets = response.json().get("data", [])

    # Store in MongoDB cache
    tweets_collection.update_one(
        {"query": query},
        {"$set": {"tweets": tweets, "timestamp": time.time()}},
        upsert=True
    )

    return tweets

#Function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    return "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"

#weighted scoring
def calculate_travel_score(sentiment,weather,popularity):
    sentiment_score=0
    if sentiment == "positive":
        sentiment_score = 2
    elif sentiment == "negative":
        sentiment_score == -2
    
    #weather score
    weather_score = 0
    if weather:
        condition = weather.get("condition", "").lower()
        if "clear" in condition or "sun" in condition:
            weather_score = 3
        elif "cloud" in condition:
            weather_score = 2
        elif "rain" in condition:
            weather_score = -2
        elif "snow" in condition:
            weather_score = -3
    
    #final weighted score
    travel_score = (sentiment_score*2) + (weather_score*1.5) + popularity
    return round(travel_score,2)

#Flask route to fetch and analyze tweets
@app.route('/analyze-tweets', methods=['GET'])
def analyze_tweets():
    query = request.args.get("query","travel") #default query is travel
    tweets = get_tweets(query)

    if "error" in tweets:
        return jsonify(tweets)

    location_scores = {} #store travel scores for each location
    
    analyzed_tweets = []

    for tweet in tweets:
        sentiment = analyze_sentiment(tweet["text"])
        locations = extract_locations(tweet["text"])

        # Debugging Logs
        print(f"Tweet: {tweet['text']}")
        print(f"Extracted Locations: {locations}")

        #weather info for the first detected location
        weather_info = None
        if locations:
            try:
                weather_info = get_weather(locations[0])  
            except Exception as e:
                print(f"Weather API Error: {e}")
        
        # Debugging Output
        print(f"Weather for {locations[0] if locations else 'No Location'}: {weather_info}")
        
        for location in locations:
            if location not in location_scores:
                location_scores[location] = {"count": 0, "scores": []}
        
            location_scores[location]["count"] +=1
            
            # Calculate Travel Score for this location
            score = calculate_travel_score(sentiment, weather_info, location_scores[location]["count"])
            location_scores[location]["scores"].append(score)

        analyzed_tweets.append({
            "text": tweet["text"], 
            "sentiment": sentiment, 
            "locations":locations,
            "weather":weather_info
        })


        #store in mongo
        tweets_collection.insert_one({
            "text": tweet["text"], 
            "sentiment":sentiment, 
            "locations":locations,
            "weather":weather_info
        })

    # Calculate Final Scores (Average Score for Each Location)
    final_scores = {
        location: round(sum(data["scores"]) / len(data["scores"]), 2)  # Average score
        for location, data in location_scores.items()
    }

    return jsonify({"tweets": analyzed_tweets, "travel_scores": final_scores})

@app.route('/')
def home():
    return jsonify(message="Hello from Flask!")

@app.route('/add-sample')
def add_sample():
    doc = {"place": "Barcelona", "rating": 9}
    collection.insert_one(doc)
    return jsonify(status ="sample data inserted")

@app.route('/get-sample')
def get_sample():
    docs = list(collection.find({},{"_id": 0}))
    return jsonify(data=docs)

if __name__ == '__main__':
    app.run(debug=True)
