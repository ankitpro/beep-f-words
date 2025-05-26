# cli.py (New CLI interface)
import argparse
from beep_overlay.main import process_video

def main():
    parser = argparse.ArgumentParser(description="Clean profanity from video audio and optionally add subtitles.")
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--lang", default="en", help="Language of the video")
    parser.add_argument("--model", default="medium", help="Whisper model size: tiny, base, small, medium, large")
    parser.add_argument("--download_subtitles", action="store_true", help="Download .srt subtitles")
    parser.add_argument("--output_final_video", action="store_true", help="Output final video with original and clean audio")
    parser.add_argument("--embed_subtitles", action="store_true", help="Embed subtitles into final video")

    args = parser.parse_args()

    process_video(
        video_path=args.video,
        language=args.lang,
        model_size=args.model,
        download_subtitles=args.download_subtitles,
        output_final_video=args.output_final_video,
        embed_subtitles=args.embed_subtitles
    )

if __name__ == "__main__":
    main()