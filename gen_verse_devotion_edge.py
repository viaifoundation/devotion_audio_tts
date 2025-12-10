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
# Cleaned Chinese devotional text (replace with actual text)
TEXT = """
神与你同在 12/10/2025 (以赛亚书 7:14)

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

# 2. Extract Verse (First parenthesis content)
verse_match = re.search(r"\((.*?)\)", TEXT)
verse_ref = verse_match.group(1).strip() if verse_match else "Unknown-Verse"

filename = filename_parser.generate_filename(verse_ref, date_str).replace(".mp3", "_edge.mp3")
OUTPUT = f"/Users/mhuo/Downloads/{filename}"
print(f"Target Output: {OUTPUT}")

# Convert Bible references in the text (e.g., '罗马书 1:17' to '罗马书 1章17節')
TEXT = convert_bible_reference(TEXT)
TEXT = convert_dates_in_text(TEXT)
TEXT = remove_space_before_god(TEXT)
# Split the text into paragraphs
paragraphs = [p.strip() for p in TEXT.strip().split("\n\n") if p.strip()]
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

TEMP_DIR = "/Users/mhuo/Downloads/" # For temp files
TEMP_FIRST = "/Users/mhuo/Downloads/temp_first_verse.mp3"
TEMP_SECOND = "/Users/mhuo/Downloads/temp_second_verse.mp3"
TEMP_THIRD = "/Users/mhuo/Downloads/temp_third_verse.mp3"
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
