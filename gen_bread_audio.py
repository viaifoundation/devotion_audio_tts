import asyncio
import sys
import edge_tts
from pydub import AudioSegment
import os
from bible_parser import convert_bible_reference

# Cleaned Chinese devotional text (replace with actual text)
TEXT = """
靈晨靈糧10月15日葛立新执事：<“恩典25”第13篇：我们的故事，他的恩典>

2005年，我带着不到三岁的女儿 Emily 第一次受邀参加基督六家举办的亲子关系讲座，在参加儿童节目时，Emily 的手被门夹伤，医生甚至诊断手指可能再也不能生长。第一次参加教会活动，就遭遇如此打击，按理说，我们可能不会再回教会。然而，神的恩典不离不弃，祂的爱在我们最脆弱的时刻彰显出来。在 Emily 伤势恢复期间，她无法去幼儿园，我又需上班，感谢教会张利萍姐妹带着女儿来帮忙照看 Emily。神的爱透过弟兄姐妹的实际行动活了出来，让我深切体会到 “爱是恒久忍耐，又有恩慈”（哥林多前书 13:4）的真实。借着这件事我们全家也经历了神的奇妙恩典 —— Emily的手不仅完全恢复，高中时还在教会国语部司琴。正如圣经所说：“神使万事互相效力，叫爱神的人得益处”（罗马书 8:28）。神的爱始终不离不弃，我们的家庭因此蒙福。
在参加良友团契组织的篮球、露营和分享等活动中，我们逐渐感受到弟兄姐妹间的关怀，也将基督六家视为自己的家。在神的带领下，2006年的感恩节，我受洗归主，正式成为神国的一员。

屬靈三代一家親！
在基督六家，从孩子的成长到我属灵生命的历程，我深深体会到神一路奇妙的带领与恩典。大女儿 Emily 和小女儿 Joy 从小参加教会活动、AWANA 服事，更有张长老和淑芬师母做孩子属灵长辈的保驾护航；我也在颜牧师和 Sharon 师母的带领下，于 2010 年加入AWANA 服事至 2023 年，期间不仅孩子们得以成长，我的灵命也不断被造就。之后，神呼召我将服事重点转向社区，参与爱邻社的社区宣教事工，将神的爱带到社区，荣耀神的名。
从 2005 年到 2025 年，二十年间，神的恩典一路同行。我们的家庭蒙祝福，两个孩子在基督六家的大家庭中成长，人生各阶段都有神的看顾与引导。回望过去，我满心感恩神的不离不弃，也感谢教会弟兄姐妹一路同行与支持。正如诗篇所言：“你们要称谢耶和华，因他本为善，他的慈爱永远长存。”（诗篇 136:1）在恩典 25 的庆典中，我怀着感恩的心，将我们全家的故事献给神，见证祂的信实与恩典。
基督六家 —— 神的家，我们永远的家。
"""

# Convert Bible references in the text (e.g., '罗马书 1:17' to '罗马书 1章17節')
TEXT = convert_bible_reference(TEXT)

# Split the text into paragraphs
paragraphs = [p.strip() for p in TEXT.strip().split("\n\n") if p.strip()]
first_paragraphs = [paragraphs[0]]  # First paragraph (introduction)
second_paragraphs = ["\n\n".join(paragraphs[1:])]  # All remaining paragraphs (main content)

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
FIRST_VOICE = "zh-CN-YunyangNeural"  # First voice (introduction)
SECOND_VOICE = "zh-CN-XiaoyiNeural"  # Second voice (main content)
OUTPUT = "/Users/mhuo/Downloads/bread_1015.mp3"
TEMP_DIR = "/Users/mhuo/Downloads/"  # For temp files
TEMP_FIRST = "/Users/mhuo/Downloads/temp_first_bread.mp3"
TEMP_SECOND = "/Users/mhuo/Downloads/temp_second_bread.mp3"

async def generate_audio(text, voice, output_file):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_file)

async def main():
    # Generate and collect first voice audio segments (for first paragraph)
    first_segments = []
    for i, para in enumerate(first_paragraphs):
        temp_file = f"{TEMP_DIR}temp_first_bread_{i}.mp3"
        await generate_audio(para, FIRST_VOICE, temp_file)
        print(f"✅ Generated first voice chunk {i}: {temp_file}")
        segment = AudioSegment.from_mp3(temp_file)
        first_segments.append(segment)
        os.remove(temp_file)  # Clean up immediately

    # Concatenate first segments with short silence between
    silence = AudioSegment.silent(duration=500)  # 0.5s pause; adjust as needed
    first_audio = AudioSegment.empty()
    for i, segment in enumerate(first_segments):
        first_audio += segment
        if i < len(first_segments) - 1:  # Add silence between segments, not after last
            first_audio += silence

    # Generate and collect second voice audio segments (for remaining paragraphs)
    second_segments = []
    for i, para in enumerate(second_paragraphs):
        temp_file = f"{TEMP_DIR}temp_second_bread_{i}.mp3"
        await generate_audio(para, SECOND_VOICE, temp_file)
        print(f"✅ Generated second voice chunk {i}: {temp_file}")
        segment = AudioSegment.from_mp3(temp_file)
        second_segments.append(segment)
        os.remove(temp_file)  # Clean up immediately

    # Concatenate second segments with short silence between
    second_audio = AudioSegment.empty()
    for i, segment in enumerate(second_segments):
        second_audio += segment
        if i < len(second_segments) - 1:  # Add silence between segments, not after last
            second_audio += silence

    # Combine first and second with a pause between sections
    combined_audio = first_audio + silence + second_audio
    combined_audio.export(OUTPUT, format="mp3")
    print(f"✅ Combined audio saved: {OUTPUT}")

if __name__ == "__main__":
    asyncio.run(main())
