# Folder: beep_overlay/main.py
import whisper
from better_profanity import profanity
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os

MODEL_SIZE = "medium"


def transcribe_audio(audio_path, model_size=MODEL_SIZE, input_language="en"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language=input_language, word_timestamps=True)
    return result['segments']


def detect_profanities(segments):
    profanity.load_censor_words()
    beep_timestamps = []
    for segment in segments:
        for word in segment['words']:
            if profanity.contains_profanity(word['word']):
                beep_timestamps.append((word['start'], word['end']))
    return beep_timestamps


def overlay_beeps(audio_path, beeps, output_audio_path, beep_sound_path="assets/beep.wav"):
    original = AudioFileClip(audio_path)
    beep_audio = AudioFileClip(beep_sound_path)

    clips = []
    current_time = 0

    for start, end in beeps:
        if current_time < start:
            clips.append(original.subclip(current_time, start))

        duration = end - start
        repeat_count = int(duration / beep_audio.duration) + 1
        beep_clip = concatenate_audioclips([beep_audio] * repeat_count).subclip(0, duration)
        clips.append(beep_clip)
        current_time = end

    if current_time < original.duration:
        clips.append(original.subclip(current_time, original.duration))

    final_audio = concatenate_audioclips(clips)
    final_audio.write_audiofile(output_audio_path, fps=44100)