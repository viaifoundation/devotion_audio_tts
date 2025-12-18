import asyncio
import sys
import edge_tts
from pydub import AudioSegment
import os
from bible_parser import convert_bible_reference
from date_parser import convert_dates_in_text
from text_cleaner import clean_text
import filename_parser
import re
from datetime import datetime

TTS_RATE = "+10%"  # Speed up by 10%

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

# Cleaned Chinese devotional text (replace with actual text)
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
    filename = filename_parser.generate_filename(verse_ref, date_str, extracted_prefix).replace(".mp3", "_edge.mp3")
else:
    filename = f"{date_str}_edge.mp3"
OUTPUT_DIR = os.path.join(os.getcwd(), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, filename)
print(f"Target Output: {OUTPUT_PATH}")

# Convert Bible references in the text (e.g., '罗马书 1:17' to '罗马书 1章17節')
TEXT = convert_bible_reference(TEXT)
TEXT = convert_dates_in_text(TEXT)
TEXT = clean_text(TEXT)
# Split the text into paragraphs
paragraphs = [p.strip() for p in re.split(r'\n{2,}', TEXT.strip()) if p.strip()]
first_paragraphs = [paragraphs[0]] # First paragraph (introduction)
second_paragraphs = [paragraphs[1]] # Second paragraph
third_paragraphs = [paragraphs[2]] # Third paragraph
fourth_paragraphs = ["\n\n".join(paragraphs[3:-1])] # Paragraphs between 3rd and last
fifth_paragraphs = [paragraphs[-1]] # Last paragraph
"""
Locale,ShortName,Gender,Voice Personalities,Content Categories
zh-CN,zh-CN-XiaoxiaoNeural,Female,Warm,"News, Novel"
zh-CN,zh-CN-XiaoyiNeural,Female,Lively,"Cartoon, Novel"
zh-CN,zh-CN-YunjianNeural,Male,Passion,"Sports, Novel"
zh-CN,zh-CN-YunxiNeural,Male,"Lively, Sunshine",Novel
zh-CN,zh-CN-YunxiaNeural,Male,Cute,"Cartoon, Novel"
zh-CN,zh-CN-YunyangNeural,Male,"Professional, Reliable",News
zh-CN-liaoning,zh-CN-liaoning-XiaobeiNeural,Female,Humorous,Dialect
zh-CN-shaanxi,zh-CN-shaanxi-XiaoniNeural,Female,Bright,Dialect
zh-HK,zh-HK-HiuGaaiNeural,Female,"Friendly, Positive",General
zh-HK,zh-HK-HiuMaanNeural,Female,"Friendly, Positive",General
zh-HK,zh-HK-WanLungNeural,Male,"Friendly, Positive",General
zh-TW,zh-TW-HsiaoChenNeural,Female,"Friendly, Positive",General
zh-TW,zh-TW-HsiaoYuNeural,Female,"Friendly, Positive",General
zh-TW,zh-TW-YunJheNeural,Male,"Friendly, Positive",General
"""
# Voice settings
FIRST_VOICE = "zh-CN-YunxiNeural" # First voice (introduction)
SECOND_VOICE = "zh-CN-XiaoyiNeural" # Second voice (second paragraph)
THIRD_VOICE = "zh-CN-YunyangNeural" # Third voice (third paragraph)
FOURTH_VOICE = "zh-CN-XiaoxiaoNeural" # Fourth voice (paragraphs between 3rd and last)
FIFTH_VOICE = "zh-CN-YunxiaNeural" # Fifth voice (last paragraph)
#THIRD_VOICE = "zh-CN-XiaoxiaoNeural" # Second voice (second paragraph)

TEMP_DIR = OUTPUT_DIR + os.sep # For temp files
TEMP_FIRST = os.path.join(OUTPUT_DIR, "temp_first_verse.mp3")
TEMP_SECOND = os.path.join(OUTPUT_DIR, "temp_second_verse.mp3")
TEMP_THIRD = os.path.join(OUTPUT_DIR, "temp_third_verse.mp3")

# Alias for backward compatibility with main()
OUTPUT = OUTPUT_PATH
async def generate_audio(text, voice, output_file):
    print(f"DEBUG: Text to read: {text[:100]}...")
    # print(f"DEBUG: Generating audio for text: '{text[:50]}...' (len={len(text)})")
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=TTS_RATE)
    await communicate.save(output_file)
async def main():
    # Group paragraphs
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

    # Voice mapping
    voices = [FIRST_VOICE, SECOND_VOICE, THIRD_VOICE, FOURTH_VOICE, FIFTH_VOICE]
    section_titles = ["Intro", "Scripture 1", "Scripture 2", "Main Body", "Prayer"]
    
    print(f"Processing {len(logical_sections)} logical sections...")
    final_segments = []
    global_p_index = 0

    for i, section_paras in enumerate(logical_sections):
        title = section_titles[i] if i < len(section_titles) else f"Section {i+1}"
        print(f"--- Section {i+1}: {title} ---")
        
        section_audio = AudioSegment.empty()
        silence_between_paras = AudioSegment.silent(duration=700) # Edge TTS often returns 24k or 44.1k, pydub handles mixing usually

        for j, para in enumerate(section_paras):
            voice = voices[global_p_index % len(voices)]
            print(f"  > Part {i+1}.{j+1} - {voice} ({len(para)} chars)")
            global_p_index += 1
            
            # Edge TTS requires temp file
            temp_file = f"{TEMP_DIR}temp_v{i}_p{j}.mp3"
            await generate_audio(para, voice, temp_file)
            
            try:
                segment = AudioSegment.from_mp3(temp_file)
                section_audio += segment
                if j < len(section_paras) - 1:
                    section_audio += silence_between_paras
            finally:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        
        final_segments.append(section_audio)

    # Combine all sections
    final = AudioSegment.empty()
    silence_sections = AudioSegment.silent(duration=1000)

    for i, seg in enumerate(final_segments):
        final += seg
        if i < len(final_segments) - 1:
            final += silence_sections

    # Metadata extraction
    PRODUCER = "VI AI Foundation"
    TITLE = TEXT.strip().split('\n')[0]

    final.export(OUTPUT, format="mp3", tags={'title': TITLE, 'artist': PRODUCER})
    print(f"✅ Combined audio saved: {OUTPUT}")

if __name__ == "__main__":
    asyncio.run(main())
