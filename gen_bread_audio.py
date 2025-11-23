
import asyncio
import sys
import edge_tts
from pydub import AudioSegment
import os
from bible_parser import convert_bible_reference

# Cleaned Chinese devotional text (replace with actual text)
TEXT = """
靈晨靈糧11月21日Jerry长老：<“恩典25”第40篇：圆上帝的梦>

感谢神给我们预备了连续40天的见证数算神在基督六家的恩典！明天下午3点，基督六家教会将迎来25周年的庆典！愿神带领基督六家的弟兄姊妹们不仅经历主恩，更愿意摆上自己作为器皿为神使用 — 一起圆上帝的梦！

2013 年年初，当黎牧师和张长老多次鼓励我出来接受长老职分的时候，我一直不敢拒绝，因为怕神不喜悦，但也一直不敢答应，因为神没发话。直到 5 月份一天的夜里，神亲自对我说话： “Jerry, It is not about your dream, it is about my dream on you.” 当我听到这句话的时候，心中吃下了定心丸：我要定位成为上帝的器皿，圆上帝通过我的梦，做成祂喜悦的工。

这个梦是关于”人人传福音”！黎牧师非常注重随时随地地传福音，给我很好的榜样。经过多年的网宣学习，当遇到了疫情的特殊历史事情，我特别感受到神特别的引领要抓住机遇落实网络宣教。感谢神！借助于 “网宣5分钟” 和 “福音5分钟” 的不断摸索和实践，神不仅带领基督六家最终成就了 “福音 500 分” 的网宣集体见证，也给教会预备了两位优秀的年轻传道人！教会更是在这个基础上推行 “十字传讲好消息” 的福音紮马步训练和在此基础上的 “四点八字传福音” 门训，算是在推动 “人人传福音” 的异象上有了不一样的开启和摸索。谢谢神的供应和指引！

这个梦是关于“国度的传承”！感谢神使用黎牧师的国度胸怀，坚持在基督六家教会培养年轻的同工，解决了许多华人教会没有解决好的年轻化和传承的问题。我深知华人教会在传福音和年轻化这两点上的硬核需要，也知道神给的托付，要在这一块上做出示范型的见证 —— 做好继承也做好创新，并为向更年轻化的传承打好根基。神带领我们在疫情前就定下了教会的 MVP，在平行双轨（儿童到英文部的英文 “轨” 和包括粤语部和国语部的中文 “轨”）的运行机制中，分别定下了 NGS（下一代事工策略）和 NLT（仆人领导力培训）的战略并付诸实践。在具体实施层面，通过 Church Center 的建立提供教会的骨架支撑，更是通过 “做个 6G 基督徒” 的倡导，逐步在牧养层面落实属灵层面的传承，为更深更远关于承传的发展打下根基。

这个梦是关于“健康的门训”！主耶稣颁布的大使命的核心是关于做主的门徒。受洗只是一个门徒的开始，更需要健康的门训的跟进。教会在过去许多年不断摸索的 CROSS 门训模式逐渐成型也在成熟中。教会不仅要带领人在核心 Core 课程上有基要真理的学习，受洗加入神的国度，也要让属灵的孩子在主内通过必修 Required 课程全面健康不偏食地健康成长并长大，更要参与教会能提供的各类优化 Optimized 课程的培训。在如此 “内聚于基督” 受训的基础上，相信更可以 “外散到世界” 去服事。教会强调每个基督徒从 personal 到public 层面都能参与到国度的服事 Serve。如此通过 CROSS 门训系统受训的肢体相信可以更好为主使用，“一生一世” 与主同行，“且要住在耶和华的殿中，直到永远”。

感谢神带领我在基督六家成长！我也深知需要尽量效法上一代人的属灵榜样，把上帝托付的梦勇往直前去耕耘去摆上。我在 2018 年 6 月从职场退出就一边牧会，一边参与在圣言讲道及研经学院和随后的达拉斯神学院接受进一步装备。我感谢神，赐给我一个同心合意的长执和教牧团队，大家齐心协力带领教会一同参与圆梦的行动！ 

愿神拣选带领一代代一批批的子民参与愿上帝托付之梦！求神不断赐下恩典带领基督六家在年轻化和传福音门训上不断成长！迎接下一个蒙神喜悦发展的 25 年！

左一为Jerry（2012年第一次参与美中短宣）
2022年1月2日履职执行长老
左一为Jerry（欢送Pastor Theron）
上山祷告中

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
#SECOND_VOICE = "zh-HK-HiuGaaiNeural"  # First voice (introduction)
#FIRST_VOICE = "zh-HK-WanLungNeural"  # Second voice (main content)
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
#FIRST_VOICE = "zh-CN-YunyangNeural"  # First voice (introduction)
#SECOND_VOICE = "zh-CN-XiaoxiaoNeural"  # Second voice (main content)
#SECOND_VOICE = "zh-HK-WanLungNeural"  # First voice (introduction)
#FIRST_VOICE = "zh-HK-HiuGaaiNeural"  # Second voice (main content)
OUTPUT = "/Users/mhuo/Downloads/bread_1121.mp3"
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
