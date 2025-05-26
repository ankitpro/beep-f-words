# Folder: beep_overlay/streamlit_ui.py
import streamlit as st
import tempfile
import os
from beep_overlay.main import transcribe_audio, detect_profanities, overlay_beeps
from beep_overlay.utils import extract_audio, add_audio_to_video, add_subtitles_to_video


def main():
    st.set_page_config(page_title="Profanity Beep Overlay", layout="wide")
    st.title("🎥 Profanity Beep Overlay Tool")

    uploaded_file = st.file_uploader("Upload a movie/video file", type=["mp4", "mov", "mkv"])
    language = st.selectbox("Select video language", ["en", "hi", "fr", "es"], index=0)

    model_size = st.selectbox("Whisper model size", ["tiny", "base", "small", "medium", "large"],
                               help="Larger models = better accuracy but more time.")

    download_subs = st.checkbox("Download Subtitles")
    download_clean_video = st.checkbox("Download video with clean and original audio tracks")
    download_sub_video = st.checkbox("Download video with subtitles embedded")

    if uploaded_file:
        st.success(f"Uploaded file: {uploaded_file.name}")
        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = os.path.join(tmpdir, uploaded_file.name)
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())

            audio_path = os.path.join(tmpdir, "audio.wav")
            clean_audio_path = os.path.join(tmpdir, "clean_audio.wav")
            subtitle_path = os.path.join(tmpdir, "subs.srt")
            clean_video_path = os.path.join(tmpdir, "clean_video.mp4")
            subtitled_video_path = os.path.join(tmpdir, "video_with_subs.mp4")

            with st.status("Extracting audio..."):
                extract_audio(video_path, audio_path)
            st.success("Audio extracted successfully.")

            with st.status("Transcribing and detecting profanities..."):
                segments = transcribe_audio(audio_path, model_size)
                beeps = detect_profanities(segments)
            st.success(f"Transcription complete. Profanities found: {len(beeps)}")

            with st.status("Creating cleaned audio with beeps..."):
                overlay_beeps(audio_path, beeps, clean_audio_path)
            st.success("Clean audio created.")

            if download_clean_video:
                with st.status("Merging new and original audio into video..."):
                    add_audio_to_video(video_path, clean_audio_path, clean_video_path)
                # st.video(clean_video_path)
                st.download_button("Download Clean Video", open(clean_video_path, "rb"), file_name="clean_video.mp4")

            if download_subs:
                with open(subtitle_path, "w") as subf:
                    for seg in segments:
                        subf.write(f"{seg['id'] + 1}\n{format_time(seg['start'])} --> {format_time(seg['end'])}\n{seg['text']}\n\n")
                st.download_button("Download Subtitles (.srt)", open(subtitle_path, "rb"), file_name="subtitles.srt")

            if download_sub_video:
                with st.status("Attaching subtitles to video..."):
                    add_subtitles_to_video(video_path, subtitle_path, subtitled_video_path)
                # st.video(subtitled_video_path)
                st.download_button("Download Video with Subtitles", open(subtitled_video_path, "rb"), file_name="video_with_subs.mp4")
            
            if download_sub_video & download_clean_video:
                with st.status("Merging new and original audio into video..."):
                    add_audio_to_video(video_path, clean_audio_path, clean_video_path)
                with st.status("Attaching subtitles to video..."):
                    add_subtitles_to_video(clean_video_path, subtitle_path, subtitled_video_path)
                # st.video(clean_video_path)
                st.download_button("Download Video with Subtitles", open(subtitled_video_path, "rb"), file_name="video_with_subs.mp4")


def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"