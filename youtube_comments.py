import requests

def get_video_comments(video_id, api_key, max_results=100):
    comments = []
    channel_name = "Unknown Channel"

    # Fetch video details to get channel name
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    video_params = {
        "part": "snippet",
        "id": video_id,
        "key": api_key
    }

    video_response = requests.get(video_url, params=video_params)
    if video_response.status_code == 200:
        video_data = video_response.json()
        items = video_data.get("items")
        if items and "snippet" in items[0]:
            channel_name = items[0]["snippet"]["channelTitle"]

    # Fetch comments
    comment_url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": api_key,
        "textFormat": "plainText",
        "maxResults": 100,
    }

    while len(comments) < max_results:
        response = requests.get(comment_url, params=params)
        if response.status_code != 200:
            print(f"Failed to get comments: {response.text}")
            break

        data = response.json()
        for item in data.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
            if len(comments) >= max_results:
                break

        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break

    return comments, channel_name
