
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
纪念神的成就 (诗篇 85:2) 12/11/2025

法利赛人听见耶稣堵住了撒都该人的口，他们就聚集。内中有一个人是律法师，要试探耶稣，就问他说：“夫子，律法上的诫命，哪一条是最大的呢？”耶稣对他说：“你要尽心、尽性、尽意爱主－你的　神。这是诫命中的第一，且是最大的。其次也相仿，就是要爱人如己。这两条诫命是律法和先知一切道理的总纲。”
(马太福音 22:34-40 和合本)
他回答：“你要全心、全性、全意爱主你的　神。
(马太福音 22:37 新译本)
你们若常在我里面，我的话也常在你们里面，凡你们所愿意的，祈求，就给你们成就。你们多结果子，我父就因此得荣耀，你们也就是我的门徒了。我爱你们，正如父爱我一样；你们要常在我的爱里。你们若遵守我的命令，就常在我的爱里，正如我遵守了我父的命令，常在他的爱里。
(约翰福音 15:7-10 和合本)
你们若住在我里面，我的话也留在你们里面；无论你们想要什么，祈求，就给你们成就。这样，你们结出很多果子，我父就因此得荣耀，你们也就是我的门徒了。父怎样爱我，我也怎样爱你们；你们要住在我的爱里。如果你们遵守我的命令，就必定住在我的爱里，正像我遵守了我父的命令，住在他的爱里一样。
(约翰福音 15:7-10 新译本)

耶和华啊，你已经向你的地施恩，
救回被掳的雅各。
你赦免了你百姓的罪孽，
遮盖了他们一切的过犯。 
（细拉） 
(诗篇 85:1-2 和合本)
你赦免了你子民的罪孽，
遮盖了他们的一切罪恶。 （细拉）
(诗篇 85:2 新译本)


纪念神的成就

犹太教敬拜的重要一环是纪念神做过的事。神把以色列人带出埃及之后，吩咐人们记住他的话，告诉他们“要殷勤教训你的儿女。无论你坐在家里，行在路上，躺下，起来，都要谈论。”‭‭（申命记‬ ‭6:7‬）

以色列人被告诫要不断地记念神的作为、神的属性、神的话语。 

因此，在诗篇85:2中，诗篇作者通过反思神的宽恕来纪念神： 

“你赦免了你百姓的罪孽， 遮盖了他们一切的过犯。”（诗篇‬ ‭85:2‬）
 
以色列人一再犯罪悖逆神，神也一再赦免他们。诗篇85的作者为了让以色列人不忘神的大恩大德，就创作了这首诗，提醒每个反复诵读诗歌的人，记住神的怜悯、宽恕、大能和慈爱。 

诗篇作者似乎懂得，有意记念神做过的事，是一种行之有效的操练——因此我们应当参与其中。 

纪念神帮助我们思考神的恩典和爱； 
纪念神使我们确信通过耶稣能与神同在； 
纪念神让我们对神忠实地成就他的应许充满盼望； 
纪念神增强我们对他和他话语的信心； 
纪念神使我们敬拜神已成就的、感谢神将要成就的。

养成记念的习惯将使我们的心思意念专注于神的身上，并使我们的心与他的恩典紧密相连。

那么，有哪些事情你可以特意反思和感恩神呢？以下是一些可以帮助你开始做的建议：

记住，他派他的独生子为世人的罪而死； 
记住，他创造了世界，因此要为此而赞美他； 
记住，他用充满你的圣灵提醒你他的话语，使你变得更像耶稣； 
记住，他对你的恩典和慈爱。

祷告—
主啊，请赦免我曾经犯过的错。我知道我有时把事情搞砸，但我也知道你是宽恕儿女的父亲。在我前进的路上，请帮助我学习、成长，并变得更好。因为你，我成为新造的，我的过错也不再制约我。主啊，感谢你。
奉主耶稣的名，
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
