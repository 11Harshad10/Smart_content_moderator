from googleapiclient.discovery import build

# Add your YouTube API key here
YOUTUBE_API_KEY = "AIzaSyAigYNebSPho9k9IHVAB1EfZisHCA2k_AE"

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Function to get comments from a video
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

# Replace with your video ID
video_id = "CC2VWC2uKXU"  # Your video ID

# Fetch and print comments
comments = get_video_comments(video_id)
for idx, comment in enumerate(comments, start=1):
    print(f"{idx}. {comment}")

