# Devotion Audio TTS

This project generates text-to-speech (TTS) audio for Chinese Bible devotionals using multiple providers: **Microsoft Edge TTS**, **Google Cloud TTS (Gemini)**, and **Alibaba Cloud Qwen**.

## Project Structure

### Edge TTS (Default)
- `gen_devotion_audio_edge.py`: Generates devotional audio (intro + main).
- `gen_bread_audio_edge.py`: Generates bread devotional audio.
- `gen_verse_devotion_edge.py`: Generates verse-focused audio.
- `requirements-edge.txt`: Dependencies for Edge TTS.

### Other Providers
- **Gemini (Google)**: See [README-gemini.md](README-gemini.md).
- **Qwen (Alibaba)**: See [README-qwen.md](README-qwen.md).

### Shared Utilities
- `bible_parser.py`: Converts Bible references (e.g., "罗马书 1:17" to "罗马书 1 章 17 節").
- `date_parser.py`: Parses dates.
- `text_cleaner.py`: Cleans text.

## Python Environments

This project uses `pyenv` for environment management.

### Edge TTS Environments
- **Recommended**: `edge-tts-env` (Python 3.12.12)
  ```bash
  pyenv activate edge-tts-env
  pip install -r requirements-edge.txt
  ```
- **Previous**: `tts-venv` (Python 3.14.0t) – *Legacy environment used previously.*

### Gemini TTS Environment
- `gemini-tts-env` (Python 3.12.12)
  ```bash
  pyenv activate gemini-tts-env
  pip install -r requirements-gemini.txt
  ```

### Qwen TTS Environment
- `qwen-tts-mlx` (Python 3.12.12)

## Usage (Edge TTS)

1. **Activate Environment**:
   ```bash
   pyenv activate edge-tts-env
   ```

2. **Update Text**:
   Edit the `TEXT` variable in `gen_devotion_audio_edge.py`, `gen_bread_audio_edge.py`, or `gen_verse_devotion_edge.py`.

3. **Run Script**:
   ```bash
   python gen_devotion_audio_edge.py
   ```

   Output audio will be saved to `~/Downloads/`.

## Dependencies (Edge TTS)
- `edge-tts`: Microsoft Edge TTS API.
- `pydub`: Audio processing.
- `ffmpeg`: Required by pydub (`brew install ffmpeg`).

## License
MIT License

