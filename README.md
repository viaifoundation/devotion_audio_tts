# Devotion Audio TTS

A unified toolset for generating Chinese Bible devotional audio using state-of-the-art TTS providers: **Microsoft Edge TTS**, **Google Gemini/Cloud TTS**, **Alibaba Qwen TTS**, and **CosyVoice**.

## Overview

This project provides Python scripts to generate high-quality audio for:
- Daily Devotionals
- Verse of the Day (VOTD)
- "Bread" Audio (Daily portion)

It supports automatic filename generation based on the Bible verse and date found in the text.

## Supported Providers

| Provider | Script Prefix | Key Features | Setup |
| :--- | :--- | :--- | :--- |
| **Edge TTS** | `gen_*_edge.py` | **Free**, High Quality, No API Key | `pip install edge-tts` |
| **Google Gemini** | `gen_*_gemini.py` | Professional, Google Cloud | `gcloud auth application-default login` |
| **Alibaba Qwen** | `gen_*_qwen.py` | Concise, Neural | `DASHSCOPE_API_KEY` env var |
| **CosyVoice** | `gen_*_cosy.py` | Offline/Local capable (300M model) | `torch`, `modelscope` |

## Environment Setup (Recommended)

It is highly recommended to use `pyenv` to manage Python versions and virtual environments to avoid conflicts.

### 1. Prerequisites (Install Pyenv & FFmpeg)

**macOS** (via Homebrew):
```bash
brew update
brew install pyenv pyenv-virtualenv ffmpeg
```
*After installation, follow the instructions printed in your terminal to add pyenv to your shell profile (e.g., `~/.zshrc` or `~/.bash_profile`).*

**Linux** (Ubuntu/Debian example):
```bash
# Install build dependencies
sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev ffmpeg

# Install pyenv
curl https://pyenv.run | bash
```
*Follow the on-screen instructions to add pyenv to your shell configuration.*

### 2. Step-by-Step Guide

Refer to the commands below to set up the environment for this project (using Python 3.12.12).

```bash
# 1. Install Python 3.12.12 (this exact patch version)
pyenv install 3.12.12

# 2. Create a virtual environment named "tts-qwen-env" using Python 3.12.12
pyenv virtualenv 3.12.12 tts-qwen-env

# 3. Activate the virtual environment
pyenv activate tts-qwen-env

# (You’ll see the prompt change to something like: (tts-qwen-env) % )

# 4. When you’re done working, deactivate it
pyenv deactivate
```

### 3. Helpful Commands

```bash
# Optional but recommended: set the virtualenv to be automatically activated
# when you cd into your project directory (e.g. ~/projects/tts-qwen)
# Create/set local version for the project folder:
cd ~/path/to/your/project
pyenv local tts-qwen-env
# Now every time you cd into this folder, it will auto-activate

# List all pyenv-managed Python versions
pyenv versions

# List all virtual environments
pyenv virtualenvs

# Delete the virtualenv if you ever need to (be careful!)
pyenv uninstall tts-qwen-env

# Check which Python/pip you’re currently using (should point inside the venv when activated)
which python
which pip
python --version
```

## Quick Start

### 1. Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/viaifoundation/devotion_audio_tts.git
cd devotion_audio_tts
pip install -r requirements.txt
```

### 2. Generate Verse of the Day (VOTD)

Choose your preferred provider script (e.g., Edge TTS):

1.  Open `gen_verse_devotion_edge.py`
2.  Update the `TEXT` variable with your devotional content.
3.  Run the script:

```bash
python gen_verse_devotion_edge.py
```

The audio will be generated in your `~/Downloads` folder with a filename like:
`VOTD_John-3-16_2025-12-09_edge.mp3`

### 3. Usage for Other Scripts

- **Daily Devotion**: `gen_devotion_audio_edge.py`
- **Bread Audio**: `gen_bread_audio_edge.py`

## Project Utilities

- `filename_parser.py`: Handles dynamic parsing of dates and verses to generate consistent filenames.
- `bible_parser.py`: Normalizes Chinese Bible references for better TTS pronunciation (e.g., "3:16" -> "3章16节").
- `text_cleaner.py`: Formats text, adding ensuring spacing around "God" (神).

## Requirements

Global requirements are listed in `requirements.txt`. Specific providers may have additional needs:
- **Edge**: `requirements-edge.txt`
- **Gemini**: `requirements-gemini.txt`
- **Qwen**: `requirements-qwen.txt`
- **CosyVoice**: `requirements-cosy.txt`

## License

MIT License
