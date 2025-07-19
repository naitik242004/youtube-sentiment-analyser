import requests

def get_video_comments(video_id, api_key, max_results=100):
    comments = []
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": api_key,
        "textFormat": "plainText",
        "maxResults": 100,
    }

    while len(comments) < max_results:
        response = requests.get(url, params=params)
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

    return comments
