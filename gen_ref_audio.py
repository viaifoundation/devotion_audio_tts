
import asyncio
import edge_tts
import os
import argparse

# Default "Starter Voice" settings
DEFAULT_TEXT = "大家好，这是一个参考音频，用于语音克隆模型的输入。"
DEFAULT_VOICE = "zh-CN-YunxiNeural"
OUTPUT_FILE = "assets/ref_audio/ref.wav"

async def main():
    parser = argparse.ArgumentParser(description="Generate Reference Audio for GPT-SoVITS")
    parser.add_argument("--text", type=str, default=DEFAULT_TEXT, help="Text to speak")
    parser.add_argument("--voice", type=str, default=DEFAULT_VOICE, help="Edge TTS Voice (e.g. zh-CN-YunxiNeural)")
    parser.add_argument("--output", type=str, default=OUTPUT_FILE, help="Output wav file")
    
    args = parser.parse_args()
    
    output_dir = os.path.dirname(args.output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Generating Reference Audio...")
    print(f"  Voice: {args.voice}")
    print(f"  Text:  {args.text}")
    print(f"  Output: {args.output}")
    
    communicate = edge_tts.Communicate(args.text, args.voice)
    await communicate.save(args.output)
    
    print(f"✅ Created: {args.output}")
    print("\nYou can now use this with GPT-SoVITS:")
    print(f"python gen_verse_devotion_gptsovits.py --ref-audio {args.output} --ref-text \"{args.text}\"")

if __name__ == "__main__":
    asyncio.run(main())
