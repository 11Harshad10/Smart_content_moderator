from flask import Flask, render_template, request
import joblib
from googleapiclient.discovery import build

app = Flask(__name__)

# Load model
model = joblib.load("toxic_comment_classifier.pkl")

# YouTube API Key
YOUTUBE_API_KEY = "AIzaSyAigYNebSPho9k9IHVAB1EfZisHCA2k_AE"
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Function to get comments
def get_video_comments(video_id, max_results=10):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )
    response = request.execute()

    comments = []
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments

# Function to classify comments
def classify_comments(comments):
    predictions = model.predict(comments)
    return predictions

# Route to render the HTML page
@app.route("/")
def home():
    return render_template("index.html")  # Make sure "index.html" exists inside "templates/"

# Route to handle form submission
@app.route("/analyze", methods=["POST"])
def analyze():
    video_id = request.form.get("video_id")
    comments = get_video_comments(video_id)
    predictions = classify_comments(comments)

    results = [{"comment": c, "toxic": "Toxic 🚨" if p == 1 else "Non-Toxic ✅"} for c, p in zip(comments, predictions)]

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
