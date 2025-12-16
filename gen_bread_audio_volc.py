# gen_bread_audio_volc.py
# Volcengine (ByteDance/Doubao) TTS – Daily Bread Audio (Seed-TTS V3)
# Requires VOLC_APPID and VOLC_TOKEN

import io
import os
import sys
import re
import uuid
import json
import asyncio
import gzip
import struct
import websockets
from websockets.client import connect  # Explicit import
from pydub import AudioSegment
from datetime import datetime

from bible_parser import convert_bible_reference
from text_cleaner import clean_text

# Configuration
APPID = os.getenv("VOLC_APPID", "")
TOKEN = os.getenv("VOLC_TOKEN", "")
RESOURCE_ID = "seed-tts-2.0"  
CLUSTER = "volcano_tts"

WS_URL = "wss://openspeech.bytedance.com/api/v3/tts/bidirection"

# --- Protocol Bits ---
PROTOCOL_VERSION = 0b0001
HEADER_SIZE = 0b0001
MSG_TYPE_FULL_CLIENT_REQUEST = 0b0001
MSG_TYPE_AUDIO_ONLY_RESPONSE = 0b1011
MSG_TYPE_FULL_SERVER_RESPONSE = 0b1001
MSG_TYPE_ERROR = 0b1111
MSG_TYPE_SPECIFIC_FLAGS_None = 0b0000
SERIALIZATION_METHOD_JSON = 0b0001
COMPRESSION_METHOD_GZIP = 0b0001

def pack_header(msg_type):
    # Byte 0: Version (4) | Header Size (4)
    b0 = (PROTOCOL_VERSION << 4) | HEADER_SIZE
    # Byte 1: Msg Type (4) | Flags (4) 
    b1 = (msg_type << 4) | MSG_TYPE_SPECIFIC_FLAGS_None
    # Byte 2: Serialization (4) | Compression (4)
    b2 = (SERIALIZATION_METHOD_JSON << 4) | COMPRESSION_METHOD_GZIP
    # Byte 3: Reserved
    b3 = 0x00
    return struct.pack("!BBBB", b0, b1, b2, b3)

def unpack_header(data):
    if len(data) < 4:
        return None
    b0, b1, b2, b3 = struct.unpack("!BBBB", data[:4])
    msg_type = (b1 >> 4) & 0x0F
    return msg_type

async def speak_async(text: str, voice: str) -> AudioSegment:
    if not text.strip():
        return AudioSegment.empty()

    headers = {
        "X-Api-App-Id": APPID,
        "X-Api-Access-Key": TOKEN, # Token goes here
        "X-Api-Resource-Id": RESOURCE_ID,
    }

    request_json = {
        "app": {
            "appid": APPID,
            "token": TOKEN,
            "cluster": CLUSTER
        },
        "user": {
            "uid": str(uuid.uuid4())
        },
        "audio": {
            "voice_type": voice,
            "encoding": "mp3",
            "speed_ratio": 1.0,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "submit"
        }
    }
    
    payload_json = json.dumps(request_json).encode("utf-8")
    payload_compressed = gzip.compress(payload_json)
    
    header = pack_header(MSG_TYPE_FULL_CLIENT_REQUEST)
    full_msg = header + struct.pack("!I", len(payload_compressed)) + payload_compressed

    audio_buffer = io.BytesIO()
    
    try:
        async with connect(WS_URL, extra_headers=headers) as ws:
            await ws.send(full_msg)
            
            while True:
                resp = await ws.recv()
                msg_type = unpack_header(resp)
                
                if msg_type == MSG_TYPE_AUDIO_ONLY_RESPONSE: 
                    payload_len = struct.unpack("!I", resp[4:8])[0]
                    payload = resp[8:8+payload_len]
                    
                    b2 = resp[2]
                    compression = b2 & 0x0F
                    if compression == COMPRESSION_METHOD_GZIP:
                        payload = gzip.decompress(payload)
                        
                    audio_buffer.write(payload)
                    
                elif msg_type == MSG_TYPE_FULL_SERVER_RESPONSE: 
                    payload_len = struct.unpack("!I", resp[4:8])[0]
                    payload = resp[8:8+payload_len]
                    
                    b2 = resp[2]
                    if (b2 & 0x0F) == COMPRESSION_METHOD_GZIP:
                        payload = gzip.decompress(payload)
                        
                    payload_str = payload.decode("utf-8")
                    try:
                        resp_json = json.loads(payload_str)
                        if "sequence" in resp_json and resp_json["sequence"] < 0:
                            break
                    except:
                        pass
                
                elif msg_type == MSG_TYPE_ERROR: 
                    print("❌ V3 Error Message Received")
                    try:
                        payload_len = struct.unpack("!I", resp[4:8])[0]
                        payload = resp[8:8+payload_len]
                        b2 = resp[2]
                        if (b2 & 0x0F) == COMPRESSION_METHOD_GZIP:
                            payload = gzip.decompress(payload)
                        print(f"Error Details: {payload.decode('utf-8')}")
                    except:
                        pass
                    break
                    
    except Exception as e:
        print(f"❌ WebSocket Error: {e}")
        return AudioSegment.silent(duration=500)

    audio_buffer.seek(0)
    try:
        return AudioSegment.from_mp3(audio_buffer)
    except:
        return AudioSegment.silent(duration=500)

def speak(text: str, voice: str) -> AudioSegment:
    return asyncio.run(speak_async(text, voice))

# Configuration Check
if not APPID or not TOKEN:
    print("❌ Error: Missing VOLC_APPID or VOLC_TOKEN.")
    sys.exit(1)

OUTPUT_DIR = os.path.join(os.getcwd(), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "bread_volc.mp3")

TEXT = """
灵晨灵粮12月3日罗丽芳姊妹：<“恩典25”第48篇：打通信主的“任督二脉”>
我是典型的从中国来的 “无神论“ 的理科生，国内读了本科硕士，从未接触过宗教，然后来美国读博士学位。
其实我从 2005 年左右就开始接触基督徒了，在东部大学城攻读博士学位的第二年，有一位从中部搬来的白人牧师，经常邀请留学生周末去他家吃饭。为什么他们可以那样无私的为我们付出呢？这是一个我完全理解不了的世界，也没大兴趣去了解，甚至对传教反感。
后来到南加工作，接触了台湾陈妈妈、陈爸爸，他们60岁左右，开快餐店，养育子女，非常辛苦，但是每周五晚上敞开他们的家，做美味的佳肴给大家吃。他们的喜乐和面对生活挑战时所拥有的平安让我好奇这不一样的世界，开启了我慕道的漫长之路。虽然在弟兄姊妹的帮助下，我和先生 2010 年受洗了，但是我的头脑依然没被说服神创造万物、基督是我们的救赎。我的心仍是坚硬的，所谓 “见其门，但不得入其门”。
这种慕道但不信的状态一直持续了 15 年左右。2012 年初，我搬到了湾区，加入了基督六家。2016 年，我的孩子参加了颜牧师和Sharon 师母带领的 AWANA，我也在 AWANA服侍。我愿意读经但不主动读经，愿意敬拜但不把敬拜当成最重要的事情之一。因为我不真的信，心里很虚，无法做孩子们真正属灵的老师，也无法在家里做孩子们属灵的母亲；去教会也变成很挣扎的事情，经不起各种试探如工作忙碌、家人不统一的活动的等。经常不去教会，我内心滋生愧疚，愧疚滋生逃避，逃避滋生远离。当我遇到难题时，经常转向学理（比如心理学），只依靠小我，而不是信靠主。我很少祷告，我不信也觉得自己不配，同时心中缺少谦卑。我的不信和小我的骄傲几乎完全阻断了我和天父的关系。2025 上半年，我甚至开始考虑要不要完全放弃教会，放弃游离纠结的状态，走一条其他的路。
即使这样，神永远没有放弃我这只长期迷途的羔羊。在这期间，他派了许多兄弟姊妹来引领我，他们的见证像吸铁石一样，又让我远离时不由自主地靠近，比如，近期良友B组和橄榄树小组的查经，Jerry长老和师母长久以来的呼召和为我家的祷告，利萍师母敞开的怀抱。Jerry 长老倾听我的家庭琐碎的烦恼，还帮我们立家规，为我们祈祷，让我非常感动。
如果说有一个转折点，那就是于师母教导的基督生平的课程一，这个课程一般参加者为资深基督的，我这个迷路的人在利萍师母和Linwei的帮助下，最后一个混进去了。意想不到的是，我被打通了信的任督二脉。以前对我来说，耶稣基督像一个神话故事里的人物，上完第一期的课后，他变得又真又活，兼备人性和神性，是完美的神。
感谢赞美主，我终于不在心虚，开始真诚的信靠主。我开始主动一个人读圣经，意识到我之前不信，一个主要原因是我在知识上没有预备好，没有真正的读懂圣经。我更加享受教会的各种活动。写下上面文字的时候，我们全家正参加了FVC基督徒5天4夜的家庭度假，宴信中牧师让我有许多感动。God is good。
以前我学习了许多心理学方面的知识和技巧，虽然知道，但常常做不到。我的自傲让我常常愧疚。现在，我更能谦卑下来：主啊，我有我的软弱和罪过，你却爱着这样的我。
“哥林多后书 12:9“他对我说：「我的恩典够你用的，因为我的能力是在人的软弱上显得完全。」所以，我更喜欢夸自己的软弱，好叫基督的能力覆庇我。”
期待以后在六家的大家庭中有信有靠有望的日子。
"""

if __name__ == "__main__":
    if not check_auth():
        exit(1)

    TEXT = convert_bible_reference(TEXT)
    TEXT = clean_text(TEXT)

    paragraphs = [p.strip() for p in re.split(r'\n{2,}', TEXT.strip()) if p.strip()]
    intro = paragraphs[0] if paragraphs else ""
    main = "\n".join(paragraphs[1:]) if len(paragraphs) > 1 else ""

    print("Generating introduction (Vivi)…")
    # Vivi (zh_female_vv_uranus_bigtts)
    seg_intro = speak(intro, "zh_female_vv_uranus_bigtts")

    print("Generating main content (Yunzhou)…")
    # Yunzhou (zh_male_m191_uranus_bigtts)
    seg_main = speak(main, "zh_male_m191_uranus_bigtts")

    final = seg_intro + AudioSegment.silent(duration=600) + seg_main
    final = final.set_frame_rate(24000)
    final.export(OUTPUT_PATH, format="mp3", bitrate="192k")
    print(f"Success! Saved → {OUTPUT_PATH}")
