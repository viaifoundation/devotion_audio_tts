# gen_prayer_cosy.py
# Local offline CosyVoice-300M for Prayer (Paragraph Rotation)
import torch
import numpy as np
import re
import sys
import os
import warnings
from datetime import datetime
from pydub import AudioSegment

# Silence noisy libraries
warnings.filterwarnings("ignore", category=FutureWarning, module="diffusers")
warnings.filterwarnings("ignore", category=UserWarning, module="lightning")

# Setup path to find CosyVoice (sibling directory)
COSYVOICE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../CosyVoice"))
MATCHA_PATH = os.path.join(COSYVOICE_PATH, "third_party", "Matcha-TTS")

if os.path.exists(COSYVOICE_PATH):
    sys.path.append(COSYVOICE_PATH)
    if os.path.exists(MATCHA_PATH):
        sys.path.append(MATCHA_PATH)
else:
    print(f"⚠️ Warning: CosyVoice path not found at {COSYVOICE_PATH}")
    sys.exit(1)

try:
    from cosyvoice.cli.cosyvoice import CosyVoice
except ImportError as e:
    print(f"❌ Failed to import CosyVoice: {e}")
    sys.exit(1)

from bible_parser import convert_bible_reference
from date_parser import convert_dates_in_text
from text_cleaner import clean_text
import filename_parser

print("Loading CosyVoice-300M-Instruct (local offline)...")
try:
    use_fp16 = torch.cuda.is_available()
    print(f"Loading CosyVoice-300M-Instruct... [CUDA={use_fp16}, FP16={use_fp16}]")
    cosyvoice = CosyVoice('iic/CosyVoice-300M-Instruct', fp16=use_fp16)
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("Ensure you have 'modelscope' installed.")
    sys.exit(1)

TEXT = """
“犹大地的伯利恒啊， 你在犹大诸城中并不是最小的； 因为将来有一位君王要从你那里出来， 牧养我以色列民。」”
‭‭马太福音‬ ‭2‬:‭6‬ ‭CUNPSS-神‬‬

神亲爱的主耶稣基督，我们在纪念你诞生的日子向你感恩，因你的诞生给我们带来了永活的泉源，更为我们带来了永生的盼望，主啊，我们为把你旨意传遍世界，乡音更好的为主的福音做了美好榜样，主啊，你的道路高过任何人的道路，乡音就是奉主的名走主你引领的道路，带领更多的人信主，为主做了美好的见证，主，求你为今年的乡音预备各样的资源，并𧶽不同地区同工们合一答配的心，把主的福音传到地极，我们这样的祷告，是奉主基督的名。阿们！
"""

# Generate filename dynamically
first_line = TEXT.strip().split('\n')[0]
date_match = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", TEXT)
if date_match:
    m, d, y = date_match.groups()
    date_str = f"{y}-{int(m):02d}-{int(d):02d}"
else:
    date_match = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", TEXT)
    if date_match:
        y, m, d = date_match.groups()
        date_str = f"{y}-{int(m):02d}-{int(d):02d}"
    else:
        date_str = datetime.today().strftime("%Y-%m-%d")

# 2. Extract Verse
verse_ref = filename_parser.extract_verse_from_text(TEXT)

if verse_ref:
    # Remove VOTD prefix if filename_parser adds it
    raw_filename = filename_parser.generate_filename(verse_ref, date_str)
    if raw_filename.startswith("VOTD_"):
        raw_filename = raw_filename[5:]
    filename = f"prayer_{raw_filename.replace('.mp3', '')}_cosy.mp3"
else:
    filename = f"prayer_{date_str}_cosy.mp3"

OUTPUT_DIR = os.path.join(os.getcwd(), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, filename)
print(f"Target Output: {OUTPUT_PATH}")

TEXT = convert_bible_reference(TEXT)
TEXT = convert_dates_in_text(TEXT)
TEXT = clean_text(TEXT)

paragraphs = [p.strip() for p in re.split(r'\n{2,}', TEXT.strip()) if p.strip()]

# Voice Rotation (Mixing genders and cross-lingual for variety)
voices = ["中文女", "英文男", "中文男", "日语男", "粤语女"]

def speak(text: str, voice: str) -> AudioSegment:
    print(f"   Synthesizing ({len(text)} chars) with {voice}...")
    # SFT Inference
    output_gen = cosyvoice.inference_sft(text, voice)
    
    final_audio = AudioSegment.empty()
    for item in output_gen:
        if 'tts_speech' in item:
            audio_np = item['tts_speech'].numpy()
            audio_int16 = (audio_np * 32767).astype(np.int16)
            segment = AudioSegment(
                audio_int16.tobytes(),
                frame_rate=22050, 
                sample_width=2,
                channels=1
            )
            final_audio += segment
    return final_audio

final_mix = AudioSegment.empty()
silence = AudioSegment.silent(duration=800, frame_rate=22050)

print(f"Processing {len(paragraphs)} paragraphs with voice rotation...")

for i, para in enumerate(paragraphs):
    voice = voices[i % len(voices)]
    print(f"  > Para {i+1} - {voice}")
    
    try:
        segment = speak(para, voice)
        final_mix += segment
        if i < len(paragraphs) - 1:
            final_mix += silence
    except Exception as e:
        print(f"❌ Error generating para {i}: {e}")

# Upsample to 24k for consistency
final_mix = final_mix.set_frame_rate(24000)
final_mix.export(OUTPUT_PATH, format="mp3", bitrate="192k")
print(f"✅ Saved: {OUTPUT_PATH}")
