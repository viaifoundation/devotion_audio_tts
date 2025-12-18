# gen_verse_devotion_cosy.py
# Local offline CosyVoice-300M – 5 voices for verse devotion

import torch
import numpy as np
import re
import sys
import os
import warnings
from datetime import datetime

# Silence noisy libraries
warnings.filterwarnings("ignore", category=FutureWarning, module="diffusers")
warnings.filterwarnings("ignore", category=UserWarning, module="lightning")

from pydub import AudioSegment

# Setup path to find CosyVoice (sibling directory)
# and its third_party dependencies (Matcha-TTS)
COSYVOICE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../CosyVoice"))
MATCHA_PATH = os.path.join(COSYVOICE_PATH, "third_party", "Matcha-TTS")

if os.path.exists(COSYVOICE_PATH):
    sys.path.append(COSYVOICE_PATH)
    # Also add Matcha-TTS to path as CosyVoice imports 'matcha' directly
    if os.path.exists(MATCHA_PATH):
        sys.path.append(MATCHA_PATH)
    else:
        print(f"⚠️ Warning: Matcha-TTS not found at {MATCHA_PATH}")
        print("Run: cd ../CosyVoice && git submodule update --init --recursive")
else:
    print(f"⚠️ Warning: CosyVoice path not found at {COSYVOICE_PATH}")
    print("Please clone it: git clone --recursive https://github.com/FunAudioLLM/CosyVoice.git ../CosyVoice")

try:
    from cosyvoice.cli.cosyvoice import CosyVoice
    from cosyvoice.utils.file_utils import load_wav
except ImportError as e:
    print(f"❌ Failed to import CosyVoice: {e}")
    print(f"Ensure you have cloned the repo to {COSYVOICE_PATH} and installed its requirements.")
    sys.exit(1)

from bible_parser import convert_bible_reference
from date_parser import convert_dates_in_text
from text_cleaner import clean_text
import filename_parser
import argparse

# CLI Args
if "-?" in sys.argv:
    print(f"Usage: python {sys.argv[0]} [--prefix PREFIX] [--help]")
    print("Options:")
    print("  --prefix PREFIX      Filename prefix (overrides 'FilenamePrefix' in text)")
    print("  --help, -h           Show this help")
    print("\n  (Note: You can also add 'FilenamePrefix: <Prefix>' in the input TEXT)")
    sys.exit(0)

parser = argparse.ArgumentParser()
parser.add_argument("--prefix", type=str, default=None, help="Filename prefix")
args, unknown = parser.parse_known_args()
CLI_PREFIX = args.prefix

TEXT = """
跑尽当跑的路 (希伯来书 12:2) 12/18/2025

忽然，有一大队天兵同那天使赞美　神说：
在至高之处荣耀归与　神！
在地上平安归与他所喜悦的人（有古卷：喜悦归与人）！
(路加福音 2:13-14 和合本)
忽然有一大队天兵，同那天使一起赞美　神说：
“在至高之处，荣耀归与　神！
在地上，平安归与他所喜悦的人！”
(路加福音 2:13-14 新译本)
所以，你们要自卑，服在　神大能的手下，到了时候，他必叫你们升高。你们要将一切的忧虑卸给　神，因为他顾念你们。
(彼得前书 5:6-7 和合本)
所以你们要谦卑，服在　神大能的手下，到了时候，他必叫你们升高。你们要把一切忧虑卸给　神，因为他顾念你们。
(彼得前书 5:6-7 新译本)
你们的光也当这样照在人前，叫他们看见你们的好行为，便将荣耀归给你们在天上的父。”
(马太福音 5:16 和合本)
照样，你们的光也应当照在人前，让他们看见你们的好行为，又颂赞你们在天上的父。
(马太福音 5:16 新译本)

我们既有这许多的见证人，如同云彩围着我们，就当放下各样的重担，脱去容易缠累我们的罪，存心忍耐，奔那摆在我们前头的路程，仰望为我们信心创始成终的耶稣（或译：仰望那将真道创始成终的耶稣）。他因那摆在前面的喜乐，就轻看羞辱，忍受了十字架的苦难，便坐在　神宝座的右边。
(希伯来书 12:1-2 和合本)
专一注视耶稣，就是那位信心的创造者和完成者。他因为那摆在面前的喜乐，就忍受了十字架，轻看了羞辱，现在就坐在　神宝座的右边。
(希伯来书 12:2 新译本)

跑尽当跑的路

参加赛跑时，很重要的一点就是要极目远眺并专注于终点线。如果你不经意转头去看其他的竞争对手，你的注意力就会受到干扰，甚至导致你滑倒。保持专注至关重要。 

希伯来书的作者在谈论我们的属灵生活时也是基于同样的道理。作者鼓励他的读者在奔跑天路之际，要将目光集中在耶稣身上。

当我们定睛注视耶稣，并把思想集中在他身上时，我们就会想起他的大爱和良善。定睛在耶稣身上可以帮助我们不至于灰心丧胆。

当我们的目光从耶稣身上移开时，就会失去对真正重要事物的关注。与其专注于神的使命，我们变得沉溺于周遭世界视为重要的事。我们也会因没有定睛于神的爱而失去了价值感。

希伯来书作者鼓励读者将目光集中在耶稣身上，因为耶稣是我们信心的创始成终者。他无疑是我们有信心的原因，但他也是继续使我们的心圣洁和加强我们信心的真神。

耶稣带着深邃的喜乐来忍受十字架的痛苦，因为他将自己的目光锁定于终点线上——坐在父神旁边的权威位置，并为追随他的人实现救恩的计划。我们现在全因他的忍耐才得以经历救恩的美好。

耶稣的榜样让我们能够坚持不懈、专注地跑完人生的路程。所以如果你觉得自己累了想放弃，那就花点时间祷告，思念为你付出一切的耶稣。向神祈求忍耐，这样你就能继续在你的信心中成长，并跑尽你当跑的路

祷告
神啊，感谢你为我的信心创始成终。我要把我过去的困扰、眼前的痛苦，还有我未来的考量都交托给你。让我专心定睛于你，而不是属世的纷扰和担忧。奉耶稣的名求，阿们。
"""


print("Loading CosyVoice-300M-Instruct (local offline)...")
# CosyVoice automatically handles model download via modelscope if not present
try:
    # Auto-enable FP16 if CUDA is available for speed
    use_fp16 = torch.cuda.is_available()
    print(f"Loading CosyVoice-300M-Instruct (local offline)... [CUDA={use_fp16}, FP16={use_fp16}]")
    cosyvoice = CosyVoice('iic/CosyVoice-300M-Instruct', fp16=use_fp16)
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("Ensure you have 'modelscope' installed and dependencies met.")
    sys.exit(1)



# Generate filename dynamically
# 1. Extract Date
TEXT = clean_text(TEXT)
first_line = TEXT.strip().split('\n')[0]
date_match = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", first_line)
if date_match:
    m, d, y = date_match.groups()
    date_str = f"{y}-{int(m):02d}-{int(d):02d}"
else:
    # Try YYYY-MM-DD
    date_match = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", first_line)
    if date_match:
        y, m, d = date_match.groups()
        date_str = f"{y}-{int(m):02d}-{int(d):02d}"
    else:
        date_str = datetime.today().strftime("%Y-%m-%d")

# 2. Extract Verse
# Handle both English () and Chinese （） parentheses, and both : and ： colons
verse_ref = filename_parser.extract_verse_from_text(TEXT)

if verse_ref:
    extracted_prefix = CLI_PREFIX if CLI_PREFIX else filename_parser.extract_filename_prefix(TEXT)
    filename = filename_parser.generate_filename(verse_ref, date_str, extracted_prefix).replace(".mp3", "_cosy.mp3")
else:
    filename = f"{date_str}_cosy.mp3"
OUTPUT_DIR = os.path.join(os.getcwd(), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, filename)
print(f"Target Output: {OUTPUT_PATH}")

TEXT = convert_bible_reference(TEXT)
TEXT = convert_dates_in_text(TEXT)
TEXT = clean_text(TEXT)

paragraphs = [p.strip() for p in re.split(r'\n{2,}', TEXT.strip()) if p.strip()]

# Built-in CosyVoice voices
# NOTE: CosyVoice SFT inference uses specific speaker names.
# Common ones: "中文女", "中文男", "日语男", "粤语女", "英文女", "英文男", "韩语女"
voices = ["中文女", "中文男", "英文女", "中文女", "中文男"]

def speak(text: str, voice: str) -> AudioSegment:
    print(f"DEBUG: Text to read: {text[:100]}...")
    # inference_sft returns a result iterable usually, or creates a generator
    # output format: {'tts_speech': tensor, 'samplerate': 22050}
    # It might return a generator, so we iterate
    
    print(f"   Synthesizing ({len(text)} chars) with {voice}...")
    output_gen = cosyvoice.inference_sft(text, voice)
    
    final_audio = AudioSegment.empty()
    
    # Iterate through the generator
    for item in output_gen:
        if 'tts_speech' in item:
            audio_np = item['tts_speech'].numpy()
            # Normalize float -1..1 to int16
            audio_int16 = (audio_np * 32767).astype(np.int16)
            segment = AudioSegment(
                audio_int16.tobytes(),
                frame_rate=22050, 
                sample_width=2,
                channels=1
            )
            final_audio += segment
            
    return final_audio

# Group paragraphs into 5 logical sections
if len(paragraphs) < 5:
    logical_sections = [[p] for p in paragraphs]
else:
    logical_sections = [
        [paragraphs[0]],              # Intro
        [paragraphs[1]],              # Scripture 1
        [paragraphs[2]],              # Scripture 2
        paragraphs[3:-1],             # Main Body
        [paragraphs[-1]]              # Prayer
    ]

print(f"Processing {len(logical_sections)} logical sections...")
# Voice mapping (Rotation)
# CosyVoice-300M-Instruct supports: 中文女, 中文男, 日语男, 粤语女, 英文女, 英文男, 韩语女
# We add English Male and Japanese Male because they can speak Chinese too (Cross-lingual)
voices = ["中文女", "英文男", "中文男", "日语男", "中文女"]
section_titles = ["Intro", "Scripture 1", "Scripture 2", "Main Body", "Prayer"]

final_segments = []
global_p_index = 0

for i, section_paras in enumerate(logical_sections):
    title = section_titles[i] if i < len(section_titles) else f"Section {i+1}"
    print(f"--- Section {i+1}: {title} ---")
    
    section_audio = AudioSegment.empty()
    silence_between_paras = AudioSegment.silent(duration=700, frame_rate=22050)

    for j, para in enumerate(section_paras):
        voice = voices[global_p_index % len(voices)]
        print(f"  > Part {i+1}.{j+1} - {voice}")
        global_p_index += 1
        current_segment = speak(para, voice)
        section_audio += current_segment
        
        if j < len(section_paras) - 1:
            section_audio += silence_between_paras
            
    final_segments.append(section_audio)

final = AudioSegment.empty()
silence_between_sections = AudioSegment.silent(duration=1000, frame_rate=22050)

for i, seg in enumerate(final_segments):
    final += seg
    if i < len(final_segments) - 1:
        final += silence_between_sections

# Convert to 24k for consistency with others if desired, or keep 22k
final = final.set_frame_rate(24000)
# Metadata extraction
PRODUCER = "VI AI Foundation"
TITLE = TEXT.strip().split('\n')[0]

final.export(OUTPUT_PATH, format="mp3", bitrate="192k", tags={'title': TITLE, 'artist': PRODUCER})
print(f"Success! Saved → {OUTPUT_PATH}")
