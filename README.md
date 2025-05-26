# 🔊 beep-f-words

**beep-f-words** is a Python tool to automatically:
- Detect profane words (like `f***`) in video/audio using Whisper,
- Overlay them with a beep sound using FFmpeg,
- Optionally generate subtitles,
- And clean audio while preserving the original for dual-track output.

Perfect for content creators, educators, and platforms that want to censor profanity without losing context.

---

## ✨ Features

- 🎙️ Speech-to-text transcription using OpenAI's Whisper (multilingual support)
- 🚫 Profanity detection and beep overlay
- 🎬 Video processing with FFmpeg
- 📝 Subtitles generation (optional)
- 🧠 Streamlit UI for visual interaction
- 💻 CLI interface for quick terminal use
- 🐳 Dockerized setup
- 📦 PyPI-ready package

---

## ⚙️ Installation

### 1. Clone the repo

```
git clone https://github.com/your-username/beep-f-words.git
cd beep-f-words
```

### 2. Install Python 3.11 with pyenv (recommended due to compatibility issues with 3.12)

```
brew update
brew install pyenv

# Add to shell config
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
exec "$SHELL"

# Install compatible Python version
pyenv install 3.11.9
pyenv local 3.11.9
```

### 3. Setup virtual environment using Poetry

```
poetry env use 3.11.9
poetry install --no-root
```

### 4. Fix SSL certificate issue on macOS (optional)

```
/Applications/Python\ 3.12/Install\ Certificates.command
```

## 🚀 Usage

### 🔧 CLI
```
poetry run beep-clean path/to/input_video.mp4
```

Options available:
--language for setting language (en, hi, etc.)
--model-size for Whisper model (tiny, base, small, medium, large)
--subtitles to download SRT subtitles
--output-video to download clean + original audio tracks
--burn-subtitles to embed subtitles into the output video

Example:
```
poetry run beep-clean "input.mp4" --language en --model-size base --subtitles --output-video --burn-subtitles
```

### 🖥️ Streamlit UI
Launch UI:
```
poetry run streamlit run main.streamlit.py
```
Features in UI:
1. Upload your video
2. Select Whisper model with tooltips
3. Choose language
4. Enable subtitles & audio options
5. Monitor progress with rich visuals

## 🐳 Docker (Optional)
```
docker build -t beep-f-words .
docker run -p 8501:8501 -v $PWD:/app beep-f-words
```

## 🛠️ Troubleshooting

### ❌ Error 1: Poetry project install error
```
The current project could not be installed: No file/folder found for package transcription-beep-overlay

Error1: 
Installing the current project: transcription-beep-overlay (0.1.0)
Error: The current project could not be installed: No file/folder found for package transcription-beep-overlay
If you do not want to install the current project use --no-root.
If you want to use Poetry only for dependency management but not for packaging, you can disable package mode by setting package-mode = false in your pyproject.toml file.
If you did intend to install the current project, you may need to set `packages` in your pyproject.toml file.
```
poetry install --no-root
```
Error2: 
Issues with 3.12 for pytorch and streamlit and so downgraded.

Step1: Install pyenv
```
brew update           
brew install pyenv

# Add this to your ~/.zshrc or ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Then restart shell
exec "$SHELL"
```

Step2: Install Python 3.11.x with pyenv
```
pyenv install 3.11.9
```

Step3: Use Python 3.11 for your project
```
cd /beep-f-words
pyenv local 3.11.9
```

Step4: Recreate poetry virtualenv with Python 3.11 and install dependencies.
```
poetry env use 3.11.9 
poetry install --no-root
```

Step6: Run the code again:
```
poetry run streamlit run main.streamlit.py
```
```
Fix:
```
poetry install --no-root
```

### ❌ Error 2: Python 3.12 incompatibility with PyTorch/Streamlit
Use Python 3.11.9 instead (see installation steps above)

## 🧪 Testing CLI Locally
```
poetry run beep-clean ./sample_video.mp4 --language en --model-size small
```

## 🤝 Contributing
Feel free to fork and contribute! To test locally:
1. Use Python 3.11+
2. Follow Poetry and FFmpeg setup
3. Submit PRs with clear descriptions

## 📜 License
MIT © 2025 Ankit Agarwal.

🙌 Acknowledgments
OpenAI Whisper(https://github.com/openai/whisper)
FFmpeg(https://ffmpeg.org/)
Streamlit(https://streamlit.io/)
profanity-check(https://github.com/vzhou842/profanity-check)



Let me know if you want the actual license file, deployment badge support, or GitHub Action CI template added too.