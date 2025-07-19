import streamlit as st
from youtube_comments import get_video_comments
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlparse, parse_qs

# Api key
API_KEY = "AIzaSyDybwxh7W8hyBhkFwZD_frK9Jo_ySQpFtU"  

# Streamlit app config
st.set_page_config(page_title="YouTube Sentiment Analyzer", layout="wide")
st.title("📺 YouTube Comment Sentiment Analyzer")

# Helper function to extract video ID
def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    elif parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]
        elif parsed_url.path.startswith("/embed/") or parsed_url.path.startswith("/v/"):
            return parsed_url.path.split("/")[2]
    return None

# Input from user
video_url = st.text_input("Enter YouTube Video URL")

if st.button("Analyze"):
    if video_url:
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("Invalid YouTube URL.")
        else:
            with st.spinner("Fetching comments..."):
                comments = get_video_comments(video_id, API_KEY, max_results=100)

            if not comments:
                st.warning("No comments found or error fetching comments.")
            else:
                sentiments = []
                for comment in comments:
                    blob = TextBlob(comment)
                    polarity = blob.sentiment.polarity
                    if polarity > 0:
                        sentiments.append("Positive")
                    elif polarity < 0:
                        sentiments.append("Negative")
                    else:
                        sentiments.append("Neutral")

                df = pd.DataFrame({
                    "Comment": comments,
                    "Sentiment": sentiments
                })

                st.subheader("Sample Comments with Sentiment")
                st.dataframe(df.head(10), height=300)

                st.subheader("Sentiment Distribution")
                sentiment_counts = df['Sentiment'].value_counts()
                fig, ax = plt.subplots()
                ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)
