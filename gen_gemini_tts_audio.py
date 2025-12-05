import sys
from pydub import AudioSegment
import os
from bible_parser import convert_bible_reference
from text_cleaner import remove_space_before_god
from google.cloud import texttospeech

# Cleaned Chinese devotional text (replace with actual text)
TEXT = """
靈晨靈糧11月14日纪明新弟兄：<“恩典25”第35篇：在基督里的恩典>

我于2011年通过弟兄姐妹介绍进入基督之家第六家，在这之前自己虽然已受洗成为基督徒，但因根基甚浅，甚至是没根基的基督徒，还是随着世界走，自己我行我素，从不听别人的建议，好大喜功。当我第一次看到这么多有热心、爱心和快乐单纯的弟兄姐妹，就像圣经教导的“我实在告诉你们，凡要接受上帝国的，若不像小孩子，绝不能进去。”（马可福音 10:15）这节经文真实地把我当时进到教会所看见的场景印在我心中 ，更加巧合的是碰到了一位弟兄（到教会才知道姓程名阳杰），我们是在一次远志明牧师布道会认识的，我当时认定这就我们的家了！后来良友小组分为A、B两个小组，但两个小组弟兄姐妹们的爱始终在我心中永不分离。“神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不致灭亡，反得永生。”（约翰福音‬3:16）
通过在小组团契生活和良友小组常去露营的集体生活里，我感受到弟兄们和睦同居的快乐，在纪念教会25周年感恩的历程中，自己和家人都是在主恩典中成长与度过，越是在患难中，越能体会神的恩典在其中。
我于2015被查出患有肝癌的早期发现，这本来就是不可能的事情，因为肝癌没有早期发现这一说，等到发现就是晚期了，只有等待见上帝的份了！真是感谢主，因着自己连续发高烧低烧而把主要的肝癌查出来，万事互相效力，叫爱神的人得益处。
感恩当教会知道我得癌症的信息后，马上就为我和我的家做了40天的禁食祷告，神是垂听祷告的神，在圣灵的引导和医生仔细的手术下，我得到医治和平安。耶稣说：“我去医治他。”（马太福音 8:7）；“我留下平安给你们，我把我的平安赐给你们。我所赐给你们的，不像世人所赐的。你们心里不要忧愁，也不要胆怯。”（约翰福音 14:27）在手术后的休养期间，黎牧师每周一带我上韩国祷告山祷告，使我在山上得以平静地聆听神的话，也爱上了上山祷告的生活，更加快乐地面对自己患难，为主做见证，感谢赞美主！
"""
# Convert Bible references in the text (e.g., '罗马书 1:17' to '罗马书 1章17節')
TEXT = convert_bible_reference(TEXT)
TEXT = remove_space_before_god(TEXT)
# Split the text into paragraphs
paragraphs = [p.strip() for p in TEXT.strip().split("\n\n") if p.strip()]
first_paragraphs = [paragraphs[0]] # First paragraph (introduction)
second_paragraphs = paragraphs[1:] # Remaining paragraphs as individual items (main content, split to avoid length limits)

"""
Gemini-TTS Voices (examples; use with language_code='cmn-CN' for Mandarin China):
- Achernar (Female)
- Achird (Male)
- Algenib (Male)
- Algieba (Male)
- Alnilam (Male)
- Aoede (Female)
- Autonoe (Female)
- Callirrhoe (Female)
- Charon (Male)
- Despina (Female)
- Enceladus (Male)
- Erinome (Female)
- Fenrir (Male)
- Gacrux (Female)
- Iapetus (Male)
- Kore (Female)
- Laomedeia (Female)
- Leda (Female)
- Orus (Male)
- Pulcherrima (Female)
- Puck (Male)
- Rasalgethi (Male)
- Sadachbia (Male)
- Sadaltager (Male)
- Schedar (Male)
- Sulafat (Female)
- Umbriel (Male)
- Vindemiatrix (Female)
- Zephyr (Female)
- Zubenelgenubi (Male)
Note: Chinese support is in Preview; Tianjin dialect is approximated via prompts.
"""
# Voice settings (Note: Set up Google Cloud credentials, e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json")
LANGUAGE_CODE = "cmn-CN"  # Mandarin China (Preview)
MODEL_NAME = "gemini-2.5-pro-tts"  # Gemini TTS model (adjust if needed; check docs for latest)
FIRST_VOICE = "Charon"  # Example male voice for introduction
SECOND_VOICE = "Kore"  # Example female voice for main content
#FIRST_VOICE = "Achird"  # Another male
#SECOND_VOICE = "Aoede"  # Another female
FIRST_PROMPT = "Speak in Tianjin dialect with a professional tone, fast pace, and lower tones: "  # Prompt for introduction (approximates dialect)
SECOND_PROMPT = "Speak in Tianjin dialect with a warm, lively tone: "  # Prompt for main content

OUTPUT = "/Users/mhuo/Downloads/bread_1114_gemini_tianjin.mp3"
TEMP_DIR = "/Users/mhuo/Downloads/" # For temp files

def generate_audio(text, voice, prompt, output_file):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text, prompt=prompt)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=LANGUAGE_CODE,
        name=voice,
        model_name=MODEL_NAME
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    
    # Create request with relaxed safety filters to bypass content blocks for benign text
    request = texttospeech.SynthesizeSpeechRequest(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config,
        advanced_voice_options=texttospeech.AdvancedVoiceOptions(
            relax_safety_filters=True,
        ),
    )
    
    response = client.synthesize_speech(request=request)
    
    with open(output_file, "wb") as out:
        out.write(response.audio_content)

def main():
    # Generate and collect first voice audio segments (for first paragraph)
    first_segments = []
    for i, para in enumerate(first_paragraphs):
        temp_file = f"{TEMP_DIR}temp_first_bread_{i}.mp3"
        generate_audio(para, FIRST_VOICE, FIRST_PROMPT, temp_file)
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
    # Generate and collect second voice audio segments (for remaining paragraphs)
    second_segments = []
    for i, para in enumerate(second_paragraphs):
        temp_file = f"{TEMP_DIR}temp_second_bread_{i}.mp3"
        generate_audio(para, SECOND_VOICE, SECOND_PROMPT, temp_file)
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
    # Combine first and second with a pause between sections
    combined_audio = first_audio + silence + second_audio
    combined_audio.export(OUTPUT, format="mp3")
    print(f"✅ Combined audio saved: {OUTPUT}")
if __name__ == "__main__":
    main()