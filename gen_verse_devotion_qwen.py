
# gen_verse_devotion_qwen.py
# Real Qwen3-TTS – 5 voices, works perfectly

import io
import os
import requests
import dashscope
from dashscope.audio.qwen_tts import SpeechSynthesizer
from pydub import AudioSegment

from bible_parser import convert_bible_reference
from date_parser import convert_dates_in_text
from text_cleaner import remove_space_before_god

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope.api_key:
    raise ValueError("Please set DASHSCOPE_API_KEY in ~/.secrets")

OUTPUT_PATH = "/Users/mhuo/Downloads/verse_12082025.mp3"



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

TEXT = convert_bible_reference(TEXT)
TEXT = convert_dates_in_text(TEXT)
TEXT = remove_space_before_god(TEXT)

paragraphs = [p.strip() for p in TEXT.strip().split("\n\n") if p.strip()]
# Supported Qwen-TTS voices
voices = ["Cherry", "Serena", "Ethan", "Chelsie", "Cherry"]

def chunk_text(text: str, max_len: int = 400) -> list[str]:
    if len(text) <= max_len:
        return [text]
    import re
    chunks = []
    current_chunk = ""
    parts = re.split(r'([。！？；!.?\n]+)', text)
    for part in parts:
        if len(current_chunk) + len(part) < max_len:
            current_chunk += part
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = part
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def speak(text: str, voice: str) -> AudioSegment:
    resp = SpeechSynthesizer.call(
        model="qwen-tts",
        text=text,
        voice=voice,
        format="wav",
        sample_rate=24000
    )
    if resp.status_code != 200:
        raise Exception(f"API Error: {resp.message}")
    
    # Qwen-TTS returns a URL, we need to download it
    audio_url = resp.output.audio["url"]
    audio_data = requests.get(audio_url).content
    return AudioSegment.from_wav(io.BytesIO(audio_data))

print("Generating 5 parts...")
segments = []
for i, para in enumerate(paragraphs):
    print(f"Part {i+1}/5 → {voices[i % len(voices)]}")
    
    # Check length
    if len(para) > 450:
        chunks = chunk_text(para, 400)
        print(f"  Split into {len(chunks)} chunks due to length.")
        para_segment = AudioSegment.empty()
        for chunk in chunks:
            if chunk.strip():
                para_segment += speak(chunk, voices[i % len(voices)])
        segments.append(para_segment)
    else:
        segments.append(speak(para, voices[i % len(voices)]))

final = AudioSegment.empty()
# ... (rest of concatenation)
silence = AudioSegment.silent(duration=700, frame_rate=24000)
for i, seg in enumerate(segments):
    final += seg
    if i < len(segments) - 1:
        final += silence
final.export(OUTPUT_PATH, format="mp3", bitrate="192k")
print(f"Success! Saved → {OUTPUT_PATH}")
