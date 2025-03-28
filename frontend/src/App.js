import {useEffect, useState} from "react";

function App(){
  const [query,setQuery] = useState("beach");
  const [tweets,setTweets] = useState([]);
  const [travelScores, setTravelScores] = useState({});
  const [loading,setLoading] = useState(false);
  const [error,setError] = useState("");
  


  //func to fetch tweets from flask
  const fetchTweets = async () => {
    setLoading(true);
    setError("");

    try{
      const response = await fetch(`http://127.0.0.1:5000/analyze-tweets?query=${query}`)
      const data = await response.json();

      if(data.error){
        setError(data.error);
        setTweets([]);
        setTravelScores([]);
      }else{
        setTweets(data.tweets || []);
        setTravelScores(data.travel_scores || {})
      }

    }catch (err){
      setError("Failed to fetch tweets.")
    }

    setLoading(false);
  };

  useEffect (() => {
    fetchTweets();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // useEffect(() => {
  //   fetch("http://127.0.0.1:5000/")
  //     .then((res) => res.json())
  //     .then((data) => setMessage(data.message))
  //     .catch((err) => setMessage("Error: "+ err.message));
  // }, [])

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ textAlign: "center", color: "#333" }}>🌍 Find Your Next Travel Destination</h1>

      {/* Search Bar */}
      <div style={{ display: "flex", justifyContent: "center", marginBottom: "20px" }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search a travel keyword (e.g., beach, mountains, Paris)..."
          style={{
            padding: "10px",
            fontSize: "16px",
            width: "70%",
            border: "1px solid #ccc",
            borderRadius: "5px",
          }}
        />
        <button 
          onClick={fetchTweets} 
          style={{ padding: "10px", fontSize: "16px", marginLeft: "10px", background: "#007BFF", color: "white", border: "none", borderRadius: "5px", cursor: "pointer" }}
        >
          Search
        </button>
      </div>

      {/* Loading & Error Messages */}
      {loading && <p style={{ textAlign: "center" }}>Loading travel data...</p>}
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      {/* Top Travel Destinations */}
      <h2 style={{ textAlign: "center", marginBottom: "15px" }}>🏆 Top Travel Recommendations</h2>
      {Object.keys(travelScores).length > 0 ? (
        <div>
          {Object.entries(travelScores)
            .sort((a, b) => b[1] - a[1]) // Sort locations by highest score
            .map(([location, score], index) => (
              <div key={index} style={{ background: "#f9f9f9", padding: "15px", marginBottom: "10px", borderRadius: "8px", boxShadow: "0px 0px 5px rgba(0,0,0,0.1)" }}>
                <h3>{location}</h3>
                <p>Travel Score: <strong>{score}</strong></p>
              </div>
            ))}
        </div>
      ) : (
        <p style={{ textAlign: "center" }}>No travel recommendations found.</p>
      )}

      {/* Recent Tweets Section */}
      <h2 style={{ textAlign: "center", marginTop: "30px" }}>📰 Recent Travel Mentions</h2>
      <ul style={{ listStyleType: "none", padding: 0 }}>
        {tweets.map((tweet, index) => (
          <li key={index} style={{ background: "#fff", padding: "10px", borderBottom: "1px solid #ddd" }}>
            <p><strong>Tweet:</strong> {tweet.text}</p>
            <p><strong>Sentiment:</strong> {tweet.sentiment}</p>
            {tweet.locations.length > 0 && <p><strong>Location:</strong> {tweet.locations.join(", ")}</p>}
            {tweet.weather && tweet.weather.temperature !== undefined && (
              <p>
                <strong>Weather:</strong> {tweet.weather.temperature}°C, {tweet.weather.condition}, Humidity: {tweet.weather.humidity}%
              </p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );


}


export default App;
