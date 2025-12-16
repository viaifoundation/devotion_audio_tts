
import asyncio
import sys
import edge_tts
from pydub import AudioSegment
import os
import re
from bible_parser import convert_bible_reference
from text_cleaner import clean_text

# Cleaned Chinese devotional text (replace with actual text)
TEXT = """
靈晨靈糧12月15日吴静师母：<“恩典25”第49篇：40天禁食祷告中经历神的恩典>

借着教会这次40天禁食祷告活动，我也想分享一段我刚刚经历的40多天的回国旅程。这段经历让我深刻体会到两点：

第一，感谢神垂听祷告，让看似不可能的道路变得平坦；
第二，人生充满劳苦愁烦，唯有神是我们唯一的拯救。
自从父亲确诊胃癌后，我们全家就陷入了寝食难安的状态。那时我和姐姐每天越洋通话，商量对策，心里却充满了焦急与无助。网上查遍了资料，不仅没有得到安慰，反而徒增恐惧。在那段心力交瘁的日子里，我意识到：唯有神才是唯一的拯救。也正是那时，教会的长辈和弟兄姊妹们开始为我父亲代祷，大家的支持让我的心逐渐有了平安。

在这40天的祷告旅程中，我亲眼见证了神的恩典带领我们度过每一个难关。

首先是父亲的肺部穿刺检查。因为父亲已做过胃部手术，后续面临化疗放疗，如果肺部发现问题，将严重影响治疗方案。等待结果的过程极其煎熬，但我记得全教会的弟兄姊妹都在为此迫切祷告。感谢主，结果出来确认为良性！这让我们心里的石头落了地，只需定期复查，便可专心应对胃部治疗。

然而，术后的恢复并不顺利。父亲进食困难，伴随严重的咳嗽和呕吐。视频里看到他痛苦的样子，听到姐姐描述只能无奈地带父亲反复就医、打营养针，我心如刀绞。我开始动摇：家人如此需要我，我真的不回去吗？但理智又告诉我回国的风险——我已经八年没有回国，之前的签证曾被行政审查（Check），如今形势不明，一旦被卡住两三个月，我的工作、这边的孩子该怎么办？

在两难之间，我选择将这一切带到祷告中。经过衡量与交托，我决定凭信心踏上归途。奇妙的是，从决定回国那一刻起，办理签证、拿到护照，再到过海关顺利返美，每一个环节都有大家的祷告托住，一切顺利得出乎意料。我知道，这若不是神的保守，绝无可能。

在得知父亲生病之初，我脑海里曾闪过一句话：“关关难过，关关过。”抗癌是一场漫长的战役。有一天我和妈妈聊天，她感慨地说：“你们小时候，我盼着你们毕业我就轻松了；后来想着你们结婚了我就不操心了；再后来外婆生病，我两头跑，以为送走了外婆事情就少了，结果我自己血糖又出了问题。本想养好身体过年去旅游，现在你爸又病了……”

妈妈的话让我深感心酸。是啊，世上的劳苦愁烦永无止境，我们身为凡人，总有操不完的心，也有无法逃避的软弱。这让我更加确信，唯有在神里面，才有真正的依靠和最终的拯救。

这次回国，最让我欣慰的是看到妈妈把圣经带回了房间，她说要重新开始读经。看着国内忙碌的生活——忙着生存，忙着挣钱，在那样快节奏的环境中坚持信仰确实不易。虽然几次想给姐姐们传福音未能深入，但我愿意恒切祷告，求神亲自开路，愿他们在经历神的恩手后，能得着那份真正的安稳，享受神所赐的生命。
"""

# Convert Bible references in the text (e.g., '罗马书 1:17' to '罗马书 1章17節')
TEXT = convert_bible_reference(TEXT)
TEXT = clean_text(TEXT)

# Split the text into paragraphs
paragraphs = [p.strip() for p in re.split(r'\n{2,}', TEXT.strip()) if p.strip()]
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
"""
Locale,ShortName,Gender,Voice Personalities,Content Categories
zh-CN,zh-CN-XiaoxiaoNeural,Female,Warm,"News, Novel"
zh-CN,zh-CN-XiaoyiNeural,Female,Lively,"Cartoon, Novel"
zh-CN,zh-CN-YunjianNeural,Male,Passion,"Sports, Novel"
zh-CN,zh-CN-YunxiNeural,Male,"Lively, Sunshine",Novel
zh-CN,zh-CN-YunxiaNeural,Male,Cute,"Cartoon, Novel"
zh-CN,zh-CN-YunyangNeural,Male,"Professional, Reliable",News
zh-CN,zh-CN-XiaochenNeural,Female,Warm,General
zh-CN,zh-CN-XiaohanNeural,Female,Cheerful,"Novel, Cartoon"
zh-CN,zh-CN-XiaomoNeural,Female,Emotional,"Novel, Cartoon"
zh-CN,zh-CN-XiaoqiuNeural,Female,Lively,General
zh-CN,zh-CN-XiaoruiNeural,Female,Angry,"Novel, Cartoon"
zh-CN,zh-CN-XiaoshuangNeural,Female,Cute,"Cartoon, Novel"
zh-CN,zh-CN-XiaoxuanNeural,Female,"Chat, Assistant","Novel, CustomerService"
zh-CN,zh-CN-XiaoyanNeural,Female,Professional,"News, Novel"
zh-CN,zh-CN-XiaoyouNeural,Female,Cheerful,"Cartoon, Novel"
zh-CN,zh-CN-XiaozhenNeural,Female,Friendly,General
zh-CN,zh-CN-YunhaoNeural,Male,Professional,"News, Novel"
zh-CN,zh-CN-YunxiaoNeural,Male,Friendly,General
zh-CN,zh-CN-YunyeNeural,Male,Serious,"Novel, Narration"
zh-CN,zh-CN-YunzeNeural,Male,Calm,"Novel, Narration"
zh-CN-liaoning,zh-CN-liaoning-XiaobeiNeural,Female,Humorous,Dialect
zh-CN-shaanxi,zh-CN-shaanxi-XiaoniNeural,Female,Bright,Dialect
zh-CN-sichuan,zh-CN-sichuan-YunxiNeural,Male,Lively,Dialect
zh-CN-wuu,zh-CN-wuu-XiaotongNeural,Female,Friendly,Dialect
zh-CN-wuu,zh-CN-wuu-YunzheNeural,Male,Professional,Dialect
zh-CN-yue,zh-CN-yue-XiaoshanNeural,Female,Friendly,Dialect
zh-CN-yue,zh-CN-yue-YunSongNeural,Male,Professional,Dialect
zh-HK,zh-HK-HiuGaaiNeural,Female,"Friendly, Positive",General
zh-HK,zh-HK-HiuMaanNeural,Female,"Friendly, Positive",General
zh-HK,zh-HK-WanLungNeural,Male,"Friendly, Positive",General
zh-TW,zh-TW-HsiaoChenNeural,Female,"Friendly, Positive",General
zh-TW,zh-TW-HsiaoYuNeural,Female,"Friendly, Positive",General
zh-TW,zh-TW-YunJheNeural,Male,"Friendly, Positive",General
zh-TW,zh-TW-HanHanNeural,Female,Friendly,General
"""
# Voice settings
FIRST_VOICE = "zh-CN-XiaoxiaoNeural"  # First voice (introduction)
SECOND_VOICE = "zh-CN-YunyangNeural"  # Second voice (main content)
#FIRST_VOICE = "zh-HK-WanLungNeural"  # Second voice (main content)
#SECOND_VOICE = "zh-HK-HiuGaaiNeural"  # First voice (introduction)
#SECOND_VOICE = "zh-CN-XiaoyiNeural"  # Second voice (main content)
#FIRST_VOICE = "zh-HK-WanLungNeural"  # First voice (introduction)
#SECOND_VOICE = "zh-HK-HiuGaaiNeural"  # Second voice (main content)
#SECOND_VOICE = "zh-HK-HiuMaanNeural"  # Second voice (main content)
#SECOND_VOICE = "zh-HK-WanLungNeural"  # First voice (introduction)
#FIRST_VOICE = "zh-HK-HiuGaaiNeural"  # Second voice (main content)
#FIRST_VOICE = "zh-TW-HsiaoChenNeural"  # First voice (introduction)
#SECOND_VOICE = "zh-TW-YunJheNeural"  # Second voice (main content)
#FIRST_VOICE = "zh-CN-XiaoxiaoNeural"  # Second voice (main content)
#SECOND_VOICE = "zh-CN-YunyangNeural"  # First voice (introduction)
FIRST_VOICE = "zh-CN-YunyangNeural"  # First voice (introduction)
SECOND_VOICE = "zh-CN-XiaoxiaoNeural"  # Second voice (main content)
#SECOND_VOICE = "zh-HK-WanLungNeural"  # First voice (introduction)
#FIRST_VOICE = "zh-HK-HiuGaaiNeural"  # Second voice (main content)
first_line = "Bread_Audio"

OUTPUT_DIR = os.path.join(os.getcwd(), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "bread_20251215_edge.mp3")
TEMP_DIR = OUTPUT_DIR + os.sep  # For temp files
TEMP_FIRST = os.path.join(OUTPUT_DIR, "temp_first_bread.mp3")
TEMP_SECOND = os.path.join(OUTPUT_DIR, "temp_second_bread.mp3")

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
    combined_audio.export(OUTPUT_PATH, format="mp3")
    print(f"✅ Combined audio saved: {OUTPUT_PATH}")

if __name__ == "__main__":
    asyncio.run(main())
