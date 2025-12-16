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
# Cleaned Chinese devotional text (replace with actual text)
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
# Handle both English () and Chinese （） parentheses, and both : and ： colons
verse_ref = filename_parser.extract_verse_from_text(TEXT)

if verse_ref:
    filename = filename_parser.generate_filename(verse_ref, date_str).replace(".mp3", "_edge.mp3")
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
    print(f"DEBUG: Generating audio for text: '{text[:50]}...' (len={len(text)})")
    communicate = edge_tts.Communicate(text=text, voice=voice)
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

    final.export(OUTPUT, format="mp3")
    print(f"✅ Combined audio saved: {OUTPUT}")

if __name__ == "__main__":
    asyncio.run(main())
