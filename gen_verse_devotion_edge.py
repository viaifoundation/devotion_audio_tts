import asyncio
import sys
import edge_tts
from pydub import AudioSegment
import os
from bible_parser import convert_bible_reference
from date_parser import convert_dates_in_text
from text_cleaner import remove_space_before_god
# Cleaned Chinese devotional text (replace with actual text)
TEXT = """
你的内心是什么样？ 12/8/2025


“　神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至灭亡，反得永生。因为　神差他的儿子降世，不是要定世人的罪，乃是要叫世人因他得救。信他的人，不被定罪；不信的人，罪已经定了，因为他不信　神独生子的名。
(约翰福音 3:16-18)
凡认耶稣为　神儿子的，　神就住在他里面，他也住在　神里面。　神爱我们的心，我们也知道也信。
　神就是爱；住在爱里面的，就是住在　神里面，　神也住在他里面。
(约翰一书 4:15-16)
我赐给你们一条新命令，乃是叫你们彼此相爱；我怎样爱你们，你们也要怎样相爱。你们若有彼此相爱的心，众人因此就认出你们是我的门徒了。”
(约翰福音 13:34-35)

你要保守你心，胜过保守一切，
因为一生的果效是由心发出。
(箴言 4:23 和合本)
你要谨守你的心，胜过谨守一切，
因为生命的泉源由此而出。
(箴言 4:23 新译本)
当谨守你的心，胜过保守一切，
因为生命的泉源由心而出。
(箴言 4:23 标准译本)
要一丝不苟地守护你的心，
因为生命之泉从心中涌出。
(箴言 4:23 当代译本)

你的内心是什么样？

你可曾在做了一个糟糕的决定后自忖：“我怎么会做出那样的事？”

在旧约圣经中，人们视心为内在生命的内核，并相信它主导着思想、情绪和行为。心就是一个人的灵魂与心思意念的结合。

箴言4:23告诫我们“要保守你心”，这实际上是在说“要留心你用什么来填满你的内在生命。”

你口里会说出什么，取决于你容许入侵你心灵的是什么。而你所说的话将进而影响你的行为和决定。或许今天你还没感受到你的选择所带来的影响，但是随着时间的推移，这些决定终将影响到你的人生方向。 

那我们该如何刻意维护我们的内在生命呢？

我们的身体既然是神所造的，即意味着它最需要的是神。他就是维护我们的那一位。因此，我们所能为自己做到的最有益处的事，就是通过祷告、查经、思考神的祝福来刻意寻求神，同时邀请圣灵在我们每天的作息中对不停对我们说话。 

保守我们的心的最好方式就是把心交托给神。当我们让神成为我们生活的中心、力量的源泉时，我们所做的事也将出于他的意愿。

所以，不要在我们的日程表中给神作安排，而是要让我们的日常作息围绕着与神的关系来展开。让我们创造空间给神对我们说话，使我们重新得力。让神来医治我们生命中破碎的部分，这样我们口里说出来的话就会是良善的、鼓励人的，并能通往那丰盛且充满喜乐的生命。

祷告
主耶稣，感谢你无条件地爱着我。感谢你来到世上拯救我们。我想以你爱我的方式来爱你。我知道这并不容易，我也知道这将使我付出一些代价，但我要你在我的生命中占据首要的位置。因此，请告诉我如何保守我的心，也教我如何变得更像你。
阿们。
"""
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
OUTPUT = "/Users/mhuo/Downloads/verse_12082025.mp3"
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

    # Generate and collect fifth voice audio segments (for last paragraph)
    fifth_segments = []
    for i, para in enumerate(fifth_paragraphs):
        temp_file = f"{TEMP_DIR}temp_fifth_verse_{i}.mp3"
        await generate_audio(para, FIFTH_VOICE, temp_file)
        print(f"✅ Generated fifth voice chunk {i}: {temp_file}")
        segment = AudioSegment.from_mp3(temp_file)
        fifth_segments.append(segment)
        os.remove(temp_file) # Clean up immediately

    # Concatenate fifth segments with short silence between
    fifth_audio = AudioSegment.empty()
    for i, segment in enumerate(fifth_segments):
        fifth_audio += segment
        if i < len(fifth_segments) - 1: # Add silence between segments, not after last
            fifth_audio += silence
    # Combine all five with a pause between sections
    combined_audio = first_audio + silence + second_audio + silence + third_audio + silence + fourth_audio + silence + fifth_audio
    combined_audio.export(OUTPUT, format="mp3")
    print(f"✅ Combined audio saved: {OUTPUT}")
if __name__ == "__main__":
    asyncio.run(main())
