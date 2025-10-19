import asyncio
import sys
import edge_tts
from pydub import AudioSegment
import os
from bible_parser import convert_bible_reference

# Cleaned Chinese devotional text (replace with actual text)
TEXT = """
“我每逢想念你们，就感谢我的　神； 每逢为你们众人祈求的时候，常是欢欢喜喜地祈求。”
‭‭腓立比书‬ ‭1‬:‭3‬-‭4‬

如何培养健康的人际关系

想象你种下一粒种子。如果你想让这种子成长开花，就需适当地照顾它，为它提供足够的生长所需。

现在想想那些在困难时期支持你的人、那些鼓励你的人、那些你愿意一起享受人生的人。这些关系就像种子——如果你希望它们不仅茁壮成长，还能枝繁叶茂，那就要好好地去照顾它们。

“我每逢想念你們，就感謝我的神。”（腓立比书1:3）

我们读圣经时了解到保罗在腓立比建立了一个教会。他和教会一起生活时，人们慷慨仁慈地待他，与他共同传扬福音。即使保罗后来为了继续他的宣教使命而离开，腓立比教会仍一直支持他。

因此，保罗在被关入监牢后给腓立比人写了信。保罗本可以写下自己的苦难，但却没这么做；他反而为朋友们祷告，鼓励他们即使面对困苦和逼迫，也要继续过荣耀神的生活。保罗看到了他们所做的牺牲，并选择去感激和鼓励他们。

同样，我们可以跟对我们带来影响的人表达感谢和赞赏，以增进我们的人际关系。

我们可以为他们祷告、说一些鼓励他们的话，或者不遗余力地服侍他们。我们也可以慢下来，真正去聆听他们的心声，或者提起一些关乎对方通常被人忽视的事情并表达你的谢意。

神给了我们与周遭人建立关系的渴望。这意味着就像保罗和腓立比人一样，我们有机会相互鼓励和共同寻求神。但要做到这一点，我们必须愿意去照顾我们的人际关系；用心去经营以帮助它们成长，并且持续保持健康的状态。最好的方法之一，就是停下来为那些支持和鼓励我们的人感恩。所以，今天让我们花些时间来感谢神，感谢他带来那些为我们付出的人，并且特地为他们祷告。
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
SECOND_VOICE = "zh-CN-YunxiNeural"  # Second voice (main content)
OUTPUT = "/Users/mhuo/Downloads/verse_1018.mp3"
TEMP_DIR = "/Users/mhuo/Downloads/"  # For temp files
TEMP_FIRST = "/Users/mhuo/Downloads/temp_first_verse.mp3"
TEMP_SECOND = "/Users/mhuo/Downloads/temp_second_verse.mp3"

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
        temp_file = f"{TEMP_DIR}temp_second_verse_{i}.mp3"
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
