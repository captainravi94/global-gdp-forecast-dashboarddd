import streamlit as st
import os

st.title("🏁 Global GDP Ranking Race")

st.write(
"This animation shows how the world's largest economies evolved over time."
)

video_path = "gdp_race.mp4"

if os.path.exists(video_path):
    st.video(video_path)
else:
    st.error("Video file not found. Please place gdp_race.mp4 in the main project folder.")