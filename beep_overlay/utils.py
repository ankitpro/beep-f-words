# Folder: beep_overlay/utils.py
import subprocess
import os

def extract_audio(video_path, audio_path):
    subprocess.run(["ffmpeg", "-y", "-i", video_path, "-q:a", "0", "-map", "a", audio_path], check=True)

def add_audio_to_video(original_video_path, new_audio_path, output_path):
    subprocess.run([
        "ffmpeg", "-y", "-i", original_video_path, "-i", new_audio_path,
        "-map", "0:v", "-map", "1:a", "-map", "0:a", "-c:v", "copy", "-c:a", "aac",
        "-shortest", output_path
    ], check=True)

def add_subtitles_to_video(video_path, subtitle_path, output_path):
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path, "-vf", f"subtitles={subtitle_path}", output_path
    ], check=True)