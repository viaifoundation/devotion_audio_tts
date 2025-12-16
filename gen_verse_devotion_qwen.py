
# gen_verse_devotion_qwen.py
# Real Qwen3-TTS – 5 voices, works perfectly

import io
import os
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

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope.api_key:
    raise ValueError("Please set DASHSCOPE_API_KEY in ~/.secrets")

TEXT = """
来，看，去，告诉 (罗马书 10:14-17) 12/15/2025

马利亚说：
我心尊主为大；
我灵以　神我的救主为乐；
(路加福音 1:46-47)
因为你问安的声音一入我耳，我腹里的胎就欢喜跳动。这相信的女子是有福的！因为主对她所说的话都要应验。
(路加福音 1:44-45)


然而，人未曾信他，怎能求他呢？未曾听见他，怎能信他呢？没有传道的，怎能听见呢？若没有奉差遣，怎能传道呢？如经上所记：“报福音、传喜信的人，他们的脚踪何等佳美！”只是人没有都听从福音，因为以赛亚说：“主啊，我们所传的有谁信呢？”可见，信道是从听道来的，听道是从基督的话来的。
(罗马书 10:14-17 和合本)
可见信心是从所听的道来的，所听的道是藉着基督的话来的。
(罗马书 10:17 新译本)

来，看，去，告诉

我们所听见的会影响我们所知道的。
我们所知道的会影响我们所相信的。
我们所相信的会影响我们所行的。

这就是为什么聆听神的真理如此重要。 

“可见，信道是从听道来的，听道是从基督的话来的。”（罗马书 10:17）

在四本福音书中──马太福音、马可福音、路加福音和约翰福音──我们都可读到耶稣邀请跟随他的人“来看”、“去告诉”，以及“要听，也要明白”。

在写给罗马人的信中，保罗解释了为什么去把福音告诉别人很重要：

“因为‘凡求告主名的就必得救’。然而，人未曾信他，怎能求他呢？未曾听见他，怎能信他呢？没有传道的，怎能听见呢？若没有奉差遣，怎能传道呢？如经上所记：“报福音、传喜信的人，他们的脚踪何等佳美！”（罗马书 10:13-15）

那么这个“福音”或“喜信”是什么呢？

要真正理解“福音”这个好消息，让我们先来看看坏消息：我们全都败坏不堪。我们的罪使我们与良善圣洁的神隔绝，我们无法弥补这道鸿沟。

那么，好消息来了：神深爱我们，并已为我们开了一条出路。他道成肉身，承受与罪犯一样的死刑（尽管他是无辜的），付出了终极的代价，并通过死里复活来征服了坟墓。他已赐予我们成为属他的特权！

因此，“凡求告主名的就必得救”。

现在就花点时间感谢神赐下他的话语，让我们有能力接受他的福音。然后，祈求他向你展示如何与他人分享你的盼望，进而增强你的信心。

祷告：
主耶稣，感谢你与我分享你的生命。今天，请增强我的信心；提醒我你是谁和你的成就。即使谎言和疑惑围绕着我，也要让我的心和思想专注于你。与此同时，请给我勇气去告诉他人关于你那改变世界的爱。
奉耶稣的名，阿们。
"""

# Generate filename dynamically
# 1. Extract Date
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
    filename = filename_parser.generate_filename(verse_ref, date_str).replace(".mp3", "_qwen.mp3")
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

final.export(OUTPUT_PATH, format="mp3", bitrate="192k")
print(f"Success! Saved → {OUTPUT_PATH}")
