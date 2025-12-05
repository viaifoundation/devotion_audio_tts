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
彼此相爱 12/5/2025

天使回答说：“圣灵要临到你身上，至高者的能力要荫庇你，因此所要生的圣者必称为神的儿子（或译：所要生的，必称为圣，称为神的儿子）。
(路加福音 1:35 和合本)
天使回答：“圣灵要临到你，至高者的能力要覆庇你，因此那将要出生的圣者，必称为神的儿子。
(路加福音 1:35 新译本)
他要作雅各家的王，直到永远；他的国也没有穷尽。”
(路加福音 1:33 和合本)
他要作王统治雅各家，直到永远，他的国没有穷尽。”
(路加福音 1:33 新译本)
前行后随的众人喊着说：
和散那（原有求救的意思，在此是称颂的话）归于大卫的子孙！
奉主名来的是应当称颂的！
高高在上和散那！
(马太福音 21:9 和合本)
前呼后拥的群众喊叫着：
“‘和散那’归于大卫的子孙，
奉主名来的是应当称颂的，高天之上当唱‘和散那’。”
(马太福音 21:9 新译本)

神爱我们的心，我们也知道也信。
神就是爱；住在爱里面的，就是住在神里面，神也住在他里面。这样，爱在我们里面得以完全，我们就可以在审判的日子坦然无惧。因为他如何，我们在这世上也如何。爱里没有惧怕；爱既完全，就把惧怕除去。因为惧怕里含着刑罚，惧怕的人在爱里未得完全。我们爱，因为神先爱我们。
(约翰一书 4:16-19 和合本)
我们爱，因为神先爱我们。
(约翰壹书 4:19 新译本)
我们爱，是因为他先爱了我们。
(约翰一书 4:19 标准译本)

彼此相爱

关于我们彼此相爱，耶稣讲过两个要点。第一，我们若有彼此相爱的心，众人因此就认出我们是他的门徒（约翰福音13:35）；其次，我们在神里面合而为一，会使世人知道神差了他来到世上（约翰福音 17:23）。

耶稣说，通过追随他的人彼此相爱，世人将会知道他已经来了。我们应当如此相爱，好让不信耶稣的人感到惊讶和好奇，并想进一步了解他。 

耶稣洞悉这个世界将充满愤怒、纷争和冲突。正因如此，我们更应该像神爱我们一样去爱他人。爱他人能向世人展现，先爱我们的神是多么伟大和慈爱。

耶稣复活多年后，使徒约翰给耶稣的信徒写了三封短信。在第一封中，他谆谆告诫他们如何去爱，以及爱的重要性。约翰写道：“……爱是从神来的……神既是这样爱我们，我们也当彼此相爱……我们爱，因为神先爱我们。” （约翰一书4:7、4:11、4:19） 

他甚至进一步说：“人若说‘我爱神’，却恨他的弟兄，就是说谎话的；不爱他所看见的弟兄，就不能爱没有看见的神。” （约翰一书 4:20） 

在这关键上没有其他捷径可走。约翰对此说得相当明确，我们彼此相爱就是神的爱在我们里面的证据。所以，如果我们自称爱神，就应该致力于彼此相爱。

当你思考今天的经文时，问问自己：今天我需要向我生活中的哪些人表达爱？是否有人需要我去原谅？我可以用什么方式去爱主内的弟兄姐妹们？

祷告
神啊，感谢你向史上每一代的人都展现了同样无条件的爱。你一直邀请我们来与你亲近。这是多么美好的恩赐！今天，无论我面对什么，帮助我像你爱我一般去爱别人。让我的生命成为你的爱在世上运行的见证。奉耶稣名求，阿们。
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
OUTPUT = "/Users/mhuo/Downloads/verse_1205.mp3"
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
