# Folder: beep_overlay/utils.py
import subprocess
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def extract_audio2(video_path, audio_path):
    subprocess.run(["ffmpeg", "-y", "-i", video_path, "-q:a", "0", "-map", "a", audio_path], check=True)

def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    if not clip.audio:
        raise ValueError("Video has no audio stream.")
    clip.audio.write_audiofile(audio_path, codec="aac")
    
def add_audio_to_video(original_video_path, new_audio_path, output_path):
    video = VideoFileClip(original_video_path)
    new_audio = AudioFileClip(new_audio_path)
    video_with_new_audio = video.set_audio(new_audio)
    video_with_new_audio.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
def add_audio_to_video2(original_video_path, new_audio_path, output_path):
    subprocess.run([
        "ffmpeg", "-y", "-i", original_video_path, "-i", new_audio_path,
        "-map", "0:v", "-map", "1:a", "-map", "0:a", "-c:v", "copy", "-c:a", "aac",
        "-shortest", output_path
    ], check=True)

def add_subtitles_to_video(video_path, subtitle_path, output_path):
    video = VideoFileClip(video_path)

    # Example: basic parsing of .srt file (you can enhance this)
    subtitles = []
    with open(subtitle_path, 'r') as f:
        lines = f.read().split('\n\n')
        for block in lines:
            parts = block.strip().split('\n')
            if len(parts) >= 3:
                times = parts[1].split(' --> ')
                start = convert_srt_time(times[0])
                end = convert_srt_time(times[1])
                text = ' '.join(parts[2:])
                subtitles.append((start, end, text))

    clips = [video]
    for start, end, text in subtitles:
        txt_clip = TextClip(text, fontsize=24, color='white', bg_color='black').set_position(('center', 'bottom')).set_start(start).set_end(end)
        clips.append(txt_clip)

    final = CompositeVideoClip(clips)
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
def add_subtitles_to_video2(video_path, subtitle_path, output_path):
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path, "-vf", f"subtitles={subtitle_path}", output_path
    ], check=True)

def convert_srt_time(t):
    """Convert SRT time format (HH:MM:SS,MS) to seconds"""
    h, m, s_ms = t.split(':')
    s, ms = s_ms.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000