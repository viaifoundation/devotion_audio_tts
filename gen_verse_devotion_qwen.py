
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
from text_cleaner import remove_space_before_god
import filename_parser
import re
from datetime import datetime

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope.api_key:
    raise ValueError("Please set DASHSCOPE_API_KEY in ~/.secrets")






TEXT = """
神与你同在 (以赛亚书) 7:14 12/10/2025

因此，主自己要给你们一个兆头，必有童女怀孕生子，给他起名叫以马内利（就是　神与我们同在的意思）。
(以赛亚书 7:14)
约翰又作见证说：“我曾看见圣灵，仿佛鸽子从天降下，住在他的身上。我先前不认识他，只是那差我来用水施洗的、对我说：‘你看见圣灵降下来，住在谁的身上，谁就是用圣灵施洗的。’我看见了，就证明这是　神的儿子。”
(约翰福音 1:32-34)
　神所差来的就说　神的话，因为　神赐圣灵给他是没有限量的。父爱子，已将万有交在他手里。信子的人有永生；不信子的人得不着永生，　神的震怒常在他身上。”
(约翰福音 3:34-36 和合本)
　神所差来的那一位讲　神的话，因为　神把圣灵无限地赐给他。父爱子，已经把万有交在他手里。信子的，有永生；不信从子的，必不得见永生，　神的震怒却常在他身上。”
(约翰福音 3:34-36 新译本)


耶和华又晓谕亚哈斯说：“你向耶和华－你的　神求一个兆头：或求显在深处，或求显在高处。”亚哈斯说：“我不求；我不试探耶和华。”以赛亚说：“大卫家啊，你们当听！你们使人厌烦岂算小事，还要使我的　神厌烦吗？因此，主自己要给你们一个兆头，必有童女怀孕生子，给他起名叫以马内利（就是　神与我们同在的意思）。
(以赛亚书 7:10-15 和合本)
因此主自己必给你们一个兆头：看哪！必有童女怀孕生子；她要给他起名叫‘以马内利’。
(以赛亚书 7:14 新译本)
因此主要亲自给你们一个征兆：看哪！必有童贞女怀孕，她要生一个儿子，并称他的名为以马内利。
(以赛亚书 7:14 标准译本)
所以，主会亲自给你们一个征兆，必有童贞女怀孕生子并给他取名叫以马内利。
(以赛亚书 7:14 当代译本)


神与你同在

先知以赛亚在耶稣诞生前近 600 年写下了以赛亚书 7:14 中的预言。在当时，以色列人所做的一切都符合宗教的规则，就是没有按照神的命令去实践公义。像以赛亚时代的许多先知一样，这句话是对这种不公义的警告。但在这警告中却有一线希望，就是神会纠正一切。

在这节经文中，先知以赛亚给了以色列人一个盼望的理由，因为神的一个美好应许——他应许将提供一个兆头，并且他将来到我们当中。这正是以马内利的意思：神与我们同在。

但对今天的我们来说，“神与我们同在”又意味着什么呢？

这意味着通过定睛于耶稣并仰赖他，我们就能得享这种盼望。我们可以相信，从基督诞生到他如今在天上的统治——耶稣就是与我们同在的神。

当我们失去挚爱的人时，在我们的悲痛中他与我们同在。

当我们面对不公且无处伸冤时，在我们的愤怒中他与我们同在。

当我们经历丧失时，在我们的哀伤中他与我们同在。

当我们与他人一起庆祝时，在我们的喜乐中他与我们同在。

当我们向苦难的世界施予怜悯时，在我们的平安中他与我们同在。

还有，当他为我们照亮通往更美好的未来道路时，在我们的盼望中他与我们同在。

他与我们同在。

无论生活此刻将你带到何处——无论是好是坏——耶稣都与你同在，将你引向他。他就是神所应许的以马内利。耶稣就是与我们同在的神。

祷告：
神啊，感谢你与我同在。我知道你创造了我，并为我制定了美好的计划。请你帮助我看见你在我生命中与我同在。让我想起你在我身边的所有时刻，无论好坏。我今天愿意信靠你，并渴望与你同行。奉耶稣的名，
阿们。
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
# Try matching (Book) Chapter:Verse first (e.g. "(以赛亚书) 7:14")
verse_match = re.search(r"\((.*?)\)\s*(\d+[:：]\d+(?:[-\d+]*))", TEXT)
if verse_match:
    book = verse_match.group(1).strip()
    ref = verse_match.group(2).strip()
    verse_ref = f"{book} {ref}"
else:
    # Fallback to standard (Book Chapter:Verse)
    verse_match = re.search(r"\((.*?)\)", TEXT)
    verse_ref = verse_match.group(1).strip() if verse_match else "Unknown-Verse"

filename = filename_parser.generate_filename(verse_ref, date_str)
OUTPUT_PATH = f"/Users/mhuo/Downloads/{filename}"
print(f"Target Output: {OUTPUT_PATH}")

TEXT = convert_bible_reference(TEXT)
tEXT = convert_dates_in_text(TEXT)
TEXT = remove_space_before_god(TEXT)

paragraphs = [p.strip() for p in TEXT.strip().split("\n\n") if p.strip()]
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
