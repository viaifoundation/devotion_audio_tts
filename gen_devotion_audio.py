import asyncio
import sys
import edge_tts
from pydub import AudioSegment
import os
from bible_parser import convert_bible_reference

# Cleaned Chinese devotional text
TEXT = """
"弟兄姊妹，欢迎来到晨曦读经，今天由连梅为我们领读撒母耳记下第21章。
今日亮光：撒母耳记下21章1-2节
大卫年间有饥荒，一连三年，大卫就求问耶和华。耶和华说，这饥荒是因扫罗和他流人血之家杀死基遍人。原来这基遍人不是以色列人，乃是亚摩利人中所剩的，以色列人曾向他们起誓，不杀灭他们，扫罗却为以色列人和犹大人发热心，想要杀灭他们。
三年的饥荒临到以色列，大卫没有只是想办法解决粮食问题，而是求问耶和华。他知道这样的灾难背后必有属灵的原因。神启示他这是因为扫罗违背了以色列人与基遍人所立的约。这件事可能发生在多年以前，但罪的后果却延续到现在。这提醒我们罪不只影响个人，也会影响群体，不只影响当代，也会影响后代。今天我们个人，家庭，甚至国家所遭遇的一些困境，可能也与过去未处理的罪有关。祖先拜偶像的罪会影响后代，父母的罪会影响儿女，这不是迷信，而是属灵的定律。但感谢神，祂也提供了解决的方法，就是认罪悔改，与受害者和好。大卫没有推卸责任说这是扫罗做的，与我无关，他承担起作为君王的责任，寻求与基遍人和解。今天我们也需要为自己的罪，为家族的罪，甚至为国家社会的罪来认罪祷告。不要以为这些与我们无关，我们都是罪人，都需要神的怜悯。当我们谦卑认罪，寻求和解时，神的祝福就会临到。弟兄姊妹，如果你的生活中有持续的困境，不妨求问神是否有未处理的罪，是否有需要和解的关系，让我们勇敢面对，靠着主的恩典得到释放。

与Robbin传道同心祷告
主，感谢你是公义的神，也是怜悯的神。求你光照我们，显明我们生命中未处理的罪，帮助我们勇敢面对，真心悔改。也求你医治因罪带来的破口，恢复你的祝福在我们的生命，家庭和国家中。感谢祷告奉耶稣得胜的名祈求，阿们！"
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
FIRST_VOICE = "zh-CN-XiaoyiNeural"  # First voice (introduction)
SECOND_VOICE = "zh-CN-YunyangNeural"  # Second voice (main content)
OUTPUT = "/Users/mhuo/Downloads/devotion_1015.mp3"
TEMP_DIR = "/Users/mhuo/Downloads/"  # For temp files
TEMP_FIRST = "/Users/mhuo/Downloads/temp_first_devotion.mp3"
TEMP_SECOND = "/Users/mhuo/Downloads/temp_second_devotion.mp3"

async def generate_audio(text, voice, output_file):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_file)

async def main():
    # Generate and collect first voice audio segments (for first paragraph)
    first_segments = []
    for i, para in enumerate(first_paragraphs):
        temp_file = f"{TEMP_DIR}temp_first_devotion_{i}.mp3"
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
        temp_file = f"{TEMP_DIR}temp_second_devotion_{i}.mp3"
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
