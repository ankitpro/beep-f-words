import streamlit as st
import tempfile
import os
from beep_overlay.main import transcribe_audio, detect_profanities, overlay_beeps
from beep_overlay.utils import extract_audio, add_audio_to_video, add_subtitles_to_video, merge_audio_tracks

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

def main():
    st.set_page_config(page_title="Profanity Beep Overlay", layout="wide")
    st.title("🎥 Profanity Beep Overlay Tool")

    # Session state to persist UI
    if "app_state" not in st.session_state:
        st.session_state.app_state = "ready"

    uploaded_file = st.file_uploader("Upload a movie/video file", type=["mp4", "mov", "mkv"])
    language = st.selectbox("Select video language", ["en", "hi", "fr", "es"])
    model_size = st.selectbox("Whisper model size", ["tiny", "base", "small", "medium", "large"],
                              help="Larger models = better accuracy but more time.")
    download_subs = st.checkbox("Download Subtitles")
    download_clean_video = st.checkbox("Download video with clean and original audio tracks")
    download_sub_video = st.checkbox("Download video with subtitles embedded")
    download_combined_final = st.checkbox("Download Final Video (Clean + Original Audio + Subtitles)")

    col1, col2 = st.columns(2)
    with col1:
        start_button = st.button("🚀 Start Processing")
    with col2:
        stop_button = st.button("🛑 Stop Processing")

    log_area = st.sidebar.empty()
    progress_bar = st.sidebar.progress(0)

    def log(msg):
        log_area.write(msg)

    if stop_button:
        st.session_state.stop_processing = True
        st.warning("⚠️ Processing stop requested. Please restart for new inputs.")
        return

    # Display this info if previous processing is done
    if st.session_state.app_state == "processing_done":
        st.info("✅ Previous video processed. You can download your files below or start a new video.")

    # Only start processing if a file is uploaded and button clicked
    if uploaded_file and start_button:
        st.session_state.stop_processing = False
        st.success(f"Uploaded file: {uploaded_file.name}")
        st.session_state.app_state = "processing"

        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = os.path.join(tmpdir, uploaded_file.name)
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())

            audio_path = os.path.join(tmpdir, "audio.wav")
            clean_audio_path = os.path.join(tmpdir, "clean_audio.wav")
            subtitle_path = os.path.join(tmpdir, "subs.srt")
            clean_video_path = os.path.join(tmpdir, "clean_video.mp4")
            subtitled_video_path = os.path.join(tmpdir, "video_with_subs.mp4")
            final_combined_path = os.path.join(tmpdir, "final_combined_video.mp4")

            try:
                log("🔊 Step 1: Extracting audio...")
                extract_audio(video_path, audio_path)
                progress_bar.progress(15)
                if st.session_state.stop_processing: return

                log("🧠 Step 2: Transcribing...")
                segments = transcribe_audio(audio_path, model_size, input_language=language)
                progress_bar.progress(40)
                if st.session_state.stop_processing: return

                log("🧼 Step 3: Detecting profanities...")
                beeps = detect_profanities(segments)
                progress_bar.progress(50)
                if st.session_state.stop_processing: return

                log("📢 Step 4: Creating clean audio...")
                overlay_beeps(audio_path, beeps, clean_audio_path)
                progress_bar.progress(65)
                if st.session_state.stop_processing: return

                if download_clean_video or download_combined_final:
                    log("🎬 Step 5: Merging clean audio into video...")
                    add_audio_to_video(video_path, clean_audio_path, clean_video_path)
                    progress_bar.progress(80)
                    if download_clean_video:
                        st.download_button("⬇️ Download Clean Video", open(clean_video_path, "rb"), file_name="clean_video.mp4")

                if download_subs or download_sub_video or download_combined_final:
                    log("📝 Step 6: Generating subtitles...")
                    with open(subtitle_path, "w") as subf:
                        for seg in segments:
                            subf.write(f"{seg['id'] + 1}\n{format_time(seg['start'])} --> {format_time(seg['end'])}\n{seg['text']}\n\n")
                    progress_bar.progress(90)
                    if download_subs:
                        st.download_button("⬇️ Download Subtitles (.srt)", open(subtitle_path, "rb"), file_name="subtitles.srt")

                if download_sub_video:
                    log("🎞️ Step 7: Adding subtitles to clean video...")
                    add_subtitles_to_video(clean_video_path if download_clean_video else video_path, subtitle_path, subtitled_video_path)
                    progress_bar.progress(95)
                    st.download_button("⬇️ Download Subtitled Video", open(subtitled_video_path, "rb"), file_name="video_with_subs.mp4")

                if download_combined_final:
                    log("🎞️ Step 8: Creating final video with clean + original audio + subtitles...")
                    merge_audio_tracks(video_path, clean_audio_path, subtitle_path, final_combined_path)
                    progress_bar.progress(100)
                    st.download_button("⬇️ Download Final Combined Video", open(final_combined_path, "rb"), file_name="final_combined_video.mp4")

                log("✅ All steps completed successfully!")
                st.session_state.app_state = "processing_done"

            except Exception as e:
                st.error(f"🚨 An error occurred: {e}")
                log(f"❌ Error: {e}")
                st.session_state.app_state = "ready"

    # Show Start New Video button after processing is done
    if st.session_state.app_state == "processing_done":
        if st.button("🔄 Start New Video"):
            st.session_state.app_state = "ready"
            # st.experimental_rerun()
            st.rerun()

if __name__ == "__main__":
    main()
