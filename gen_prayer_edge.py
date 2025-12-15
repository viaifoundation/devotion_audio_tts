import asyncio
import sys
import edge_tts
from pydub import AudioSegment
import os
from bible_parser import convert_bible_reference
from date_parser import convert_dates_in_text
from text_cleaner import remove_space_before_god
import filename_parser
import re
from datetime import datetime

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
# 1. Extract Date (Try to find a date in the text, otherwise use today)
first_line = TEXT.strip().split('\n')[0]
date_match = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", TEXT) # Search in whole text for 34:8 case might assume date is elsewhere or use today
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
    filename = f"prayer_{raw_filename.replace('.mp3', '')}_edge.mp3"
else:
    filename = f"prayer_{date_str}_edge.mp3"

OUTPUT_DIR = os.path.join(os.getcwd(), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, filename)
print(f"Target Output: {OUTPUT_PATH}")

# Convert Bible references in the text
TEXT = convert_bible_reference(TEXT)
TEXT = convert_dates_in_text(TEXT)
TEXT = remove_space_before_god(TEXT)

# Split the text into paragraphs
paragraphs = [p.strip() for p in re.split(r'\n{2,}', TEXT.strip()) if p.strip()]

# Mandarin Voices for Rotation
voices = [
    "zh-CN-XiaoxiaoNeural", 
    "zh-CN-YunxiNeural", 
    "zh-CN-XiaoyiNeural", 
    "zh-CN-YunyangNeural", 
    "zh-CN-YunxiaNeural",
    "zh-CN-YunjianNeural"
]

TEMP_DIR = OUTPUT_DIR + os.sep 

async def generate_audio(text, voice, output_file):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_file)

async def main():
    final_audio = AudioSegment.empty()
    silence = AudioSegment.silent(duration=800) 

    print(f"Processing {len(paragraphs)} paragraphs with voice rotation...")
    
    for i, para in enumerate(paragraphs):
        voice = voices[i % len(voices)]
        print(f"  > Para {i+1} ({len(para)} chars) - {voice}")
        
        temp_file = f"{TEMP_DIR}temp_prayer_p{i}.mp3"
        await generate_audio(para, voice, temp_file)
        
        try:
            segment = AudioSegment.from_mp3(temp_file)
            final_audio += segment
            if i < len(paragraphs) - 1:
                final_audio += silence
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    final_audio.export(OUTPUT_PATH, format="mp3")
    print(f"✅ Saved: {OUTPUT_PATH}")

if __name__ == "__main__":
    asyncio.run(main())
