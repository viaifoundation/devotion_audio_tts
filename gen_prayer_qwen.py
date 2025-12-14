import io
import os
import requests
import dashscope
from dashscope.audio.qwen_tts import SpeechSynthesizer
from pydub import AudioSegment

from bible_parser import convert_bible_reference
from date_parser import convert_dates_in_text
from text_cleaner import remove_space_before_god
import filename_parser
import re
from datetime import datetime

# Setup API Key
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope.api_key:
    # Try reading from secrets file locally if env var not set
    secrets_path = os.path.expanduser("~/.secrets")
    if os.path.exists(secrets_path):
        with open(secrets_path, "r") as f:
            for line in f:
                if line.startswith("DASHSCOPE_API_KEY"):
                    dashscope.api_key = line.split("=")[1].strip()
                    break
    
    if not dashscope.api_key:
         print("⚠️ Warning: DASHSCOPE_API_KEY not found in env or ~/.secrets. Script may fail.")

TEXT = """
親愛的天父上帝，
我們滿心感恩來到祢面前，謝謝祢一路以來的帶領與供應。
我們感謝祢的恩典，灣區「鄉音」能順利完成 Redemption Church 的場地簽約，這一切榮耀都歸給祢。

主啊，我們也將聖地牙哥 UCSD – The Epstein Family Amphitheater 的租借與簽約過程交託在祢手中，懇求祢親自開路，保守每一個細節，按祢的時間與旨意成就。

我們為南北加州四場「鄉音」事工向祢呼求，
求祢祝福宣傳推廣、供應一切贊助與籌款需要，
賜下智慧與秩序，使節目的籌備與執行都合乎祢心意。
也懇求祢看顧所有同工及他們的家人，保守身體健康、心力更新，
使我們在祢裡面同心合意，彼此相愛，滿有平安。

主啊，願這一切事工都成為榮耀祢名、祝福人心的器皿，
讓我們一同見證祢奇妙又信實的作為。

以上禱告，奉主耶穌基督得勝的名求，阿們。

以馬內利 🙏💖
"""

# Generate filename dynamically
# 1. Extract Date
date_match = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", TEXT)
if date_match:
    m, d, y = date_match.groups()
    date_str = f"{y}-{int(m):02d}-{int(d):02d}"
else:
    # Try YYYY-MM-DD
    date_match = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", TEXT)
    if date_match:
        y, m, d = date_match.groups()
        date_str = f"{y}-{int(m):02d}-{int(d):02d}"
    else:
        date_str = datetime.today().strftime("%Y-%m-%d")

# 2. Extract Verse
# Handle both English () and Chinese （） parentheses, and both : and ： colons
verse_match = re.search(r"[\(（](.*?[\d]+[:：].*?)[\)）]", TEXT)
verse_ref = verse_match.group(1).strip() if verse_match else None

if verse_ref:
    # Remove VOTD prefix if filename_parser adds it (it often does "VOTD_...")
    raw_filename = filename_parser.generate_filename(verse_ref, date_str)
    # Strip "VOTD_" if present
    if raw_filename.startswith("VOTD_"):
        raw_filename = raw_filename[5:]
    filename = f"prayer_{raw_filename.replace('.mp3', '')}_qwen.mp3"
else:
    filename = f"prayer_{date_str}_qwen.mp3"
OUTPUT_DIR = os.getcwd()
OUTPUT_PATH = os.path.join(OUTPUT_DIR, filename)
print(f"Target Output: {OUTPUT_PATH}")

TEXT = convert_bible_reference(TEXT)
TEXT = convert_dates_in_text(TEXT)
TEXT = remove_space_before_god(TEXT)

paragraphs = [p.strip() for p in TEXT.strip().split("\n") if p.strip()]

# Supported Qwen-TTS voices
voices = ["Cherry", "Serena", "Ethan", "Chelsie"]

def speak(text: str, voice: str) -> AudioSegment:
    # Qwen Limit check? It's usually good for short paragraphs.
    resp = SpeechSynthesizer.call(
        model="qwen-tts",
        text=text,
        voice=voice,
        format="wav",
        sample_rate=24000
    )
    if resp.status_code != 200:
        raise Exception(f"API Error: {resp.message}")
    
    audio_url = resp.output.audio["url"]
    audio_data = requests.get(audio_url).content
    return AudioSegment.from_wav(io.BytesIO(audio_data))

print(f"Processing {len(paragraphs)} paragraphs with voice rotation...")

final_audio = AudioSegment.empty()
silence = AudioSegment.silent(duration=800, frame_rate=24000)

for i, para in enumerate(paragraphs):
    voice = voices[i % len(voices)]
    print(f"  > Para {i+1} ({len(para)} chars) - {voice}")
    
    try:
        segment = speak(para, voice)
        final_audio += segment
        if i < len(paragraphs) - 1:
            final_audio += silence
    except Exception as e:
        print(f"❌ Error generating para {i}: {e}")

final_audio.export(OUTPUT_PATH, format="mp3", bitrate="192k")
print(f"✅ Saved: {OUTPUT_PATH}")
