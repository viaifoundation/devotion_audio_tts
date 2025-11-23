import asyncio
import sys
import edge_tts
from pydub import AudioSegment
import os
from bible_parser import convert_bible_reference
# Cleaned Chinese devotional text (replace with actual text)
TEXT = """
赐各样安慰的神

“因我－耶和华是不改变的，所以你们雅各之子没有灭亡。
(玛拉基书 3:6 和合本)
我的弟兄们，你们落在百般试炼中，都要以为大喜乐；因为知道你们的信心经过试验，就生忍耐。但忍耐也当成功，使你们成全、完备，毫无缺欠。
(雅各书 1:2-4 和合本)

我虽然行过死荫的幽谷，
也不怕遭害，
因为你与我同在；
你的杖，你的竿，都安慰我。
(诗篇 23:4 和合本)

赐各样安慰的神

在古代以色列，牧羊人的杖和竿保护和引导羊群，甚至用来提醒羊群牧羊人就在现场。因此，大卫王（他小时候是牧羊人）用诗篇 23:4 中的比喻来传达这个真理：神是他的保护者和引导者。

大卫王多次面对死亡威胁，敌人一心想要杀死他。他也备受自己的罪恶问题和个人错误的困扰。但在这一切之中，他一再将注意力转向神的信实和神的保证。

他从哪里找到这些确据呢？

大卫王应该有深入研习希伯来文经卷，妥拉──即圣经中的前五本书，又称摩西五经。

对希伯来人来说，妥拉不仅仅是关于神的故事，也是神的话语；那是神的权威、应许和指引。大卫的生活以及他的诗篇正是基于妥拉中的教导。大卫能写下神的属性，因为：

一、他熟读神的话语。
二、他根据神的话语来经历神的信实与恩惠。

我们也可以有这样的体验──甚至更多。我们有旧约中古代先知所启示的神的话语；耶稣在世时的话语；耶稣通过新约的使徒和作者所启示的话语。换句话说，我们可以拥有大卫所拥有的：

一、我们可以熟读神的话语。
二、我们可以根据神的话语来体验神的信实与恩惠。

读一读耶稣对门徒所说的话：

“我将这些事告诉你们，是要叫你们在我里面有平安。在世上，你们有苦难；但你们可以放心，我已经胜了世界。”（约翰福音 16:33）

像大卫一样，我们没有什么可害怕的，因为神近在咫尺──他是我们的安慰。熟习圣经能帮助我们有把握地相信，神现在和将来都会信实地为爱他的人提供保护和指引；他也会与他们同在。所以，今天就下定决心将神的话深深印在心里。
"""
# Convert Bible references in the text (e.g., '罗马书 1:17' to '罗马书 1章17節')
TEXT = convert_bible_reference(TEXT)
# Split the text into paragraphs
paragraphs = [p.strip() for p in TEXT.strip().split("\n\n") if p.strip()]
first_paragraphs = [paragraphs[0]] # First paragraph (introduction)
second_paragraphs = [paragraphs[1]] # Second paragraph
third_paragraphs = [paragraphs[2]] # Third paragraph
fourth_paragraphs = ["\n\n".join(paragraphs[3:])] # All remaining paragraphs
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
FOURTH_VOICE = "zh-CN-XiaoxiaoNeural" # Fourth voice (remaining paragraphs)
#THIRD_VOICE = "zh-CN-XiaoxiaoNeural" # Second voice (second paragraph)
OUTPUT = "/Users/mhuo/Downloads/verse_1123.mp3"
TEMP_DIR = "/Users/mhuo/Downloads/" # For temp files
TEMP_FIRST = "/Users/mhuo/Downloads/temp_first_verse.mp3"
TEMP_SECOND = "/Users/mhuo/Downloads/temp_second_verse.mp3"
TEMP_THIRD = "/Users/mhuo/Downloads/temp_third_verse.mp3"
async def generate_audio(text, voice, output_file):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_file)
async def main():
    # Generate and collect first voice audio segments (for first paragraph)
    first_segments = []
    for i, para in enumerate(first_paragraphs):
        temp_file = f"{TEMP_DIR}temp_first_verse_{i}.mp3"
        await generate_audio(para, FIRST_VOICE, temp_file)
        print(f"✅ Generated first voice chunk {i}: {temp_file}")
        segment = AudioSegment.from_mp3(temp_file)
        first_segments.append(segment)
        os.remove(temp_file) # Clean up immediately
    # Concatenate first segments with short silence between
    silence = AudioSegment.silent(duration=500) # 0.5s pause; adjust as needed
    first_audio = AudioSegment.empty()
    for i, segment in enumerate(first_segments):
        first_audio += segment
        if i < len(first_segments) - 1: # Add silence between segments, not after last
            first_audio += silence
    # Generate and collect second voice audio segments (for second paragraph)
    second_segments = []
    for i, para in enumerate(second_paragraphs):
        temp_file = f"{TEMP_DIR}temp_second_verse_{i}.mp3"
        await generate_audio(para, SECOND_VOICE, temp_file)
        print(f"✅ Generated second voice chunk {i}: {temp_file}")
        segment = AudioSegment.from_mp3(temp_file)
        second_segments.append(segment)
        os.remove(temp_file) # Clean up immediately
    # Concatenate second segments with short silence between
    second_audio = AudioSegment.empty()
    for i, segment in enumerate(second_segments):
        second_audio += segment
        if i < len(second_segments) - 1: # Add silence between segments, not after last
            second_audio += silence
    # Generate and collect third voice audio segments (for remaining paragraphs)
    third_segments = []
    for i, para in enumerate(third_paragraphs):
        temp_file = f"{TEMP_DIR}temp_third_verse_{i}.mp3"
        await generate_audio(para, THIRD_VOICE, temp_file)
        print(f"✅ Generated third voice chunk {i}: {temp_file}")
        segment = AudioSegment.from_mp3(temp_file)
        third_segments.append(segment)
        os.remove(temp_file) # Clean up immediately
    # Concatenate third segments with short silence between
    third_audio = AudioSegment.empty()
    for i, segment in enumerate(third_segments):
        third_audio += segment
        if i < len(third_segments) - 1: # Add silence between segments, not after last
            third_audio += silence

    # Generate and collect fourth voice audio segments (for remaining paragraphs)
    fourth_segments = []
    for i, para in enumerate(fourth_paragraphs):
        temp_file = f"{TEMP_DIR}temp_fourth_verse_{i}.mp3"
        await generate_audio(para, FOURTH_VOICE, temp_file)
        print(f"✅ Generated fourth voice chunk {i}: {temp_file}")
        segment = AudioSegment.from_mp3(temp_file)
        fourth_segments.append(segment)
        os.remove(temp_file) # Clean up immediately

    # Concatenate fourth segments with short silence between
    fourth_audio = AudioSegment.empty()
    for i, segment in enumerate(fourth_segments):
        fourth_audio += segment
        if i < len(fourth_segments) - 1: # Add silence between segments, not after last
            fourth_audio += silence
    # Combine first, second, third and fourth with a pause between sections
    combined_audio = first_audio + silence + second_audio + silence + third_audio + silence + fourth_audio
    combined_audio.export(OUTPUT, format="mp3")
    print(f"✅ Combined audio saved: {OUTPUT}")
if __name__ == "__main__":
    asyncio.run(main())
