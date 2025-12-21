
# gen_verse_devotion_qwen.py
# Real Qwen3-TTS – 5 voices, works perfectly

import io
import os
import sys
import requests
import dashscope
from dashscope.audio.qwen_tts import SpeechSynthesizer
from pydub import AudioSegment

from bible_parser import convert_bible_reference
from date_parser import convert_dates_in_text
from text_cleaner import clean_text
import filename_parser
import re
from datetime import datetime

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
超越常规的信心 (路加福音 1:45) 12/20/2025

天使对妇女说：“不要害怕！我知道你们是寻找那钉十字架的耶稣。他不在这里，照他所说的，已经复活了。你们来看安放主的地方。快去告诉他的门徒，说他从死里复活了，并且在你们以先往加利利去，在那里你们要见他。看哪，我已经告诉你们了。”
(马太福音 28:5-7 和合本)
快去告诉他的门徒：‘他已经从死人中复活了。他会比你们先到加利利去，你们在那里必看见他。’现在我已经告诉你们了。”
(马太福音 28:7 新译本)
我告诉你们，一个罪人悔改，在天上也要这样为他欢喜，较比为九十九个不用悔改的义人欢喜更大。”
(路加福音 15:7 和合本)
我告诉你们，因为一个罪人悔改，天上也要这样为他欢乐，比为九十九个不用悔改的义人欢乐更大。
(路加福音 15:7 新译本)
妇女们就急忙离开坟墓，又害怕，又大大地欢喜，跑去要报给他的门徒。
(马太福音 28:8)

伊利莎白一听马利亚问安，所怀的胎就在腹里跳动。伊利莎白且被圣灵充满，高声喊着说：“你在妇女中是有福的！你所怀的胎也是有福的！我主的母到我这里来，这是从哪里得的呢？因为你问安的声音一入我耳，我腹里的胎就欢喜跳动。这相信的女子是有福的！因为主对她所说的话都要应验。”
(路加福音 1:41-45 和合本)
这相信主传给她的话必要成就的女子是有福的。”
(路加福音 1:45 新译本)
那相信主所说的话必定实现的女子有福了！”
(路加福音 1:45 当代译本)

超越常规的信心

当天使宣布马利亚将怀上神的儿子时，她还是一个在拿撒勒小城里过着宁静生活的少女（路加福音 1:31）。一般人要是听到这样的消息，本能的反应可能是恐惧、震惊或敬畏。然而，马利亚的反应却是相信——相信天使告诉她的是事实。她对天使说：“我是主的使女，情愿照你的话成就在我身上。”（路加福音 1:38）。 

马利亚的表姐伊利莎白目睹了她如此坚定不移的信心，在圣灵的感动下高声祝福马利亚和认可她的信心：“这相信的女子是有福的！因为主对她所说的话都要应验。”

在这些简单的话语中，我们受到提醒要将我们的信心锚定在坚定不移的真理上，那就是神会按照他的话语信实地履行他的应许。伊利莎白的宣告——“这相信的女子是有福的”——不仅仅是一个观察，也是一种当下的肯定。重点不仅在于这些应许必将实现，还在于因相信和仰赖神的计划而带来的祝福。它促使我们审视自己的信心之旅。我们是否像马利亚一样，选择顺服并仰赖于神的应许？

今天，你在祷告中寻求主之际，要对意外的祝福表示感激。祈求洞察力来识别神的手在做工，即使你的处境看来似乎完全相反。

祷告
神啊，尽管我心存疑虑和恐惧，我还是要来到你面前。无论你把我引向何方，我选择相信并仰赖你的大能和应许。求你增强并祝福我的信心。让我充满洞察力和感恩之心。奉耶稣的名，阿们。
"""


dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope.api_key:
    raise ValueError("Please set DASHSCOPE_API_KEY in ~/.secrets")



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
verse_ref = filename_parser.extract_verse_from_text(TEXT)

if verse_ref:
    extracted_prefix = CLI_PREFIX if CLI_PREFIX else filename_parser.extract_filename_prefix(TEXT)
    filename = filename_parser.generate_filename(verse_ref, date_str, extracted_prefix).replace(".mp3", "_qwen.mp3")
else:
    filename = f"{date_str}_qwen.mp3"
OUTPUT_DIR = os.path.join(os.getcwd(), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, filename)
print(f"Target Output: {OUTPUT_PATH}")

TEXT = convert_bible_reference(TEXT)
TEXT = convert_dates_in_text(TEXT)
TEXT = clean_text(TEXT)

paragraphs = [p.strip() for p in re.split(r'\n{2,}', TEXT.strip()) if p.strip()]
# Supported Qwen-TTS voices
voices = ["Cherry", "Serena", "Ethan", "Chelsie", "Cherry"]

def chunk_text(text: str, max_len: int = 400) -> list[str]:
    if len(text) <= max_len:
        return [text]
    import re
    chunks = []
    current_chunk = ""
    parts = re.split(r'([。！？；!.?\n]+)', text)
    for part in parts:
        if len(current_chunk) + len(part) < max_len:
            current_chunk += part
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = part
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def speak(text: str, voice: str) -> AudioSegment:
    print(f"DEBUG: Text to read: {text[:100]}...")
    resp = SpeechSynthesizer.call(
        model="qwen-tts",
        text=text,
        voice=voice,
        format="wav",
        sample_rate=24000
    )
    if resp.status_code != 200:
        raise Exception(f"API Error: {resp.message}")
    
    # Qwen-TTS returns a URL, we need to download it
    audio_url = resp.output.audio["url"]
    audio_data = requests.get(audio_url).content
    return AudioSegment.from_wav(io.BytesIO(audio_data))

# Group paragraphs into 5 logical sections
# 1. Intro (Title/Date)
# 2. Scripture 1
# 3. Scripture 2
# 4. Main Body (Middle paragraphs)
# 5. Prayer (Last paragraph)

if len(paragraphs) < 5:
    # Fallback if text is too short, just treat as list
    logical_sections = [[p] for p in paragraphs]
else:
    logical_sections = [
        [paragraphs[0]],              # Intro
        [paragraphs[1]],              # Scripture 1
        [paragraphs[2]],              # Scripture 2
        paragraphs[3:-1],             # Main Body (List of paragraphs)
        [paragraphs[-1]]              # Prayer
    ]

# Ensure we don't exceed available voices
num_sections = len(logical_sections)
section_titles = ["Intro", "Scripture 1", "Scripture 2", "Main Body", "Prayer"]
print(f"Processing {num_sections} logical sections...")

final_segments = []
global_p_index = 0

for i, section_paras in enumerate(logical_sections):
    title = section_titles[i] if i < len(section_titles) else f"Section {i+1}"
    print(f"--- Section {i+1}: {title} ---")
    
    section_audio = AudioSegment.empty()
    silence_between_paras = AudioSegment.silent(duration=700, frame_rate=24000)

    for j, para in enumerate(section_paras):
        # Cycle voices based on global paragraph count to match original behavior
        voice = voices[global_p_index % len(voices)]
        print(f"  > Part {i+1}.{j+1} - {voice} ({len(para)} chars)")
        global_p_index += 1
        
        # Check length and chunk if needed
        if len(para) > 450:
            chunks = chunk_text(para, 400)
            print(f"    Split into {len(chunks)} chunks due to length.")
            para_audio = AudioSegment.empty()
            for chunk in chunks:
                if chunk.strip():
                    para_audio += speak(chunk, voice)
            current_segment = para_audio
        else:
            current_segment = speak(para, voice)
            
        section_audio += current_segment
        
        # Add silence between paragraphs in the same section
        if j < len(section_paras) - 1:
            section_audio += silence_between_paras
            
    final_segments.append(section_audio)

final = AudioSegment.empty()
silence_between_sections = AudioSegment.silent(duration=1000, frame_rate=24000)

for i, seg in enumerate(final_segments):
    final += seg
    if i < len(final_segments) - 1:
        final += silence_between_sections

# Metadata extraction
PRODUCER = "VI AI Foundation"
TITLE = TEXT.strip().split('\n')[0]

final.export(OUTPUT_PATH, format="mp3", bitrate="192k", tags={'title': TITLE, 'artist': PRODUCER})
print(f"Success! Saved → {OUTPUT_PATH}")
