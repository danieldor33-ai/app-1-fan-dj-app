import streamlit as st
import requests
import datetime
import time

# Backend URL - replace with actual deployed backend URL
BACKEND_URL = "https://fan-dj-backend.example.com"

st.set_page_config(page_title="Fan DJ", layout="centered")

# Background image using base64 (can be updated with any image)
def set_background(image_url):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
        }}
        </style>
    """, unsafe_allow_html=True)

# Set background image
set_background("https://images.unsplash.com/photo-1503264116251-35a269479413")

st.title("🎧 Fan DJ - Sync Songs with Your Team")

# User Role
role = st.selectbox("Who are you?", ["Fan", "DJ"])

if role == "DJ":
    st.header("🎵 DJ Control Panel")

    # DJ Authentication
    password = st.text_input("Enter DJ password", type="password")
    correct_password = "fan2025"  # Change to your desired password

    if password != correct_password:
        st.warning("You must enter the correct password to access DJ controls.")
        st.stop()

    playlist = ["Song A", "Song B", "Song C", "Song D"]
    song_index = st.selectbox("Select song to play", range(len(playlist)), format_func=lambda i: playlist[i])
    duration = st.slider("Song duration (seconds)", 10, 300, 30)

    if st.button("▶️ Play Selected Song"):
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)

        # Send update to backend
        res = requests.post(f"{BACKEND_URL}/update_song", json={
            "current_song": playlist[song_index],
            "end_time": end_time.isoformat(),
            "song_index": song_index
        })

        if res.status_code == 200:
            st.success(f"Now playing: {playlist[song_index]}")
        else:
            st.error("Failed to update song on the server.")

elif role == "Fan":
    st.header("🙌 Fan View")
    placeholder = st.empty()

    while True:
        try:
            res = requests.get(f"{BACKEND_URL}/get_state")
            data = res.json()

            song = data["current_song"]
            end_time = datetime.datetime.fromisoformat(data["end_time"])
            remaining = int((end_time - datetime.datetime.utcnow()).total_seconds())

            if remaining < 0:
                remaining = 0

            with placeholder.container():
                st.subheader(f"🎶 Now Playing: {song}")
                st.markdown(f"**⏳ Time left: {remaining} seconds**")

            time.sleep(1)
            st.experimental_rerun()

        except Exception as e:
            st.error("Could not fetch song data. Check backend availability.")
            break
