from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from fastapi.middleware.cors import CORSMiddleware

# Load ML model and vectorizer
model = joblib.load("toxic_comment_classifier.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# YouTube API Scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Authenticate YouTube API with OAuth
def get_authenticated_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh the token
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r"C:\Users\comp\Documents\Project resources\cgptdetox\client_secret.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())
    
    return build("youtube", "v3", credentials=creds)

# FastAPI app
app = FastAPI()

# ✅ Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://127.0.0.1:5500"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request body model
class VideoRequest(BaseModel):
    video_id: str

# Function to fetch comments from YouTube
def get_video_comments(youtube, video_id, max_results=10):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )
    response = request.execute()

    comments = []
    comment_ids = []
    
    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comment_id = item["id"]  # Correct comment ID path
        comments.append(comment)
        comment_ids.append(comment_id)

    return comments, comment_ids

# Function to classify comments
def classify_comments(comments):
    transformed_comments = vectorizer.transform(comments)  # Apply vectorizer
    predictions = model.predict(transformed_comments)
    return predictions

# Function to delete toxic comments
def delete_comment(youtube, comment_id):
    try:
        youtube.comments().delete(id=comment_id).execute()
        return True
    except Exception as e:
        print(f"Failed to delete comment {comment_id}: {e}")
        return False

# ✅ API Route: Fetch comments and classify them
@app.post("/classify/")
def classify_video_comments(request: VideoRequest):
    youtube = get_authenticated_service()
    comments, _ = get_video_comments(youtube, request.video_id)
    predictions = classify_comments(comments)

    classified_comments = [
        {"comment": comment, "toxic": bool(pred)}
        for comment, pred in zip(comments, predictions)
    ]
    
    return {"comments": classified_comments}

# ✅ API Route: Delete toxic comments
@app.post("/delete-toxic/")
def delete_toxic_comments(request: VideoRequest):
    youtube = get_authenticated_service()
    comments, comment_ids = get_video_comments(youtube, request.video_id)
    predictions = classify_comments(comments)

    deleted_comments = []
    for comment, comment_id, is_toxic in zip(comments, comment_ids, predictions):
        if is_toxic:
            success = delete_comment(youtube, comment_id)
            if success:
                deleted_comments.append(comment)

    return {"deleted_comments": deleted_comments, "total_deleted": len(deleted_comments)}

# ✅ API Route: Basic check if backend is working
@app.get("/")
def read_root():
    return {"message": "Welcome to the Toxic Comment Detection API"}

# ✅ API Route: Simple prediction for frontend
class TextInput(BaseModel):
    text: str

@app.post("/predict")
async def predict_toxicity(input: TextInput):
    transformed_text = vectorizer.transform([input.text])
    prediction = model.predict(transformed_text)[0]
    return {"prediction": "Toxic" if prediction == 1 else "Not Toxic"}

# Run FastAPI if script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
