# Devotion Audio TTS – Volcengine (Doubao) Edition

Uses **ByteDance/Volcengine** (Doubao) TTS API for high-quality, expressive Chinese speech synthesis.

## Key Features
- **High Quality**: "Doubao" voices (e.g., Vivi, Yunzhou) are currently industry-leading for naturalness.
- **Cloud API**: Requires API Key (Paid service, but cheap/free tier available).
- **Fast**: Cloud-based generation is typically faster than local inference on older hardware.

## Files
- `gen_bread_audio_volc.py`: Daily Bread (2 voices)
- `gen_verse_devotion_volc.py`: Verse + Devotion + Prayer (Multi-voice)
- `requirements-volc.txt`: Dependencies

## Setup

### 1. Get Credentials
1. High to [Volcengine Console](https://console.volcengine.com/speech/app).
2. Create an App to get your **AppID**.
3. Create an Access Token to get your **Token**.
4. Standard Cluster ID is usually `volcano_tts`.

### 2. Environment Variables
Export your credentials in your shell:

```bash
export VOLC_APPID="your_appid_here"
export VOLC_TOKEN="your_token_here"
```

### 3. Installation
```bash
# Create environment
pyenv virtualenv 3.12.12 tts-volc-env
pyenv activate tts-volc-env

# Install
pip install -r requirements-volc.txt
```

## Usage

```bash
python gen_verse_devotion_volc.py
# or
python gen_bread_audio_volc.py
```

## Voices
Configured to use "Doubao 2.0" voices:
- `zh_female_vv_uranus_bigtts` (Vivi - Warm/Affectionate)
- `zh_male_m191_uranus_bigtts` (Yunzhou - Mature/Storytelling)
- `zh_female_xiaohe_uranus_bigtts` (Xiaohe - Gentle)
- `zh_male_taocheng_uranus_bigtts` (Xiaotian - Clear)
