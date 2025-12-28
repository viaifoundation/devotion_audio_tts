import os
from huggingface_hub import hf_hub_download, snapshot_download

# Paths
# We assume we are running from project root, but let's be absolute or relative to workspace
# The internal structure seems to be /workspace/GPT-SoVITS/GPT_SoVITS/pretrained_models

BASE_DIR = "/workspace/GPT-SoVITS/GPT_SoVITS/pretrained_models"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def download_gpt_sovits_base():
    print("\n--- Downloading GPT-SoVITS Base Models (lj1995/GPT-SoVITS) ---")
    ensure_dir(BASE_DIR)
    
    files = [
        "s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt",
        "s2G488k.pth",
        "s2D488k.pth"
    ]
    
    for filename in files:
        print(f"Downloading {filename}...")
        try:
            hf_hub_download(
                repo_id="lj1995/GPT-SoVITS",
                filename=filename,
                local_dir=BASE_DIR,
                local_dir_use_symlinks=False
            )
            print(f"✅ {filename} downloaded.")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")

def download_chinese_roberta():
    print("\n--- Downloading Chinese RoBERTa (hfl/chinese-roberta-wwm-ext-large) ---")
    target_dir = os.path.join(BASE_DIR, "chinese-roberta-wwm-ext-large")
    ensure_dir(target_dir)
    
    try:
        snapshot_download(
            repo_id="hfl/chinese-roberta-wwm-ext-large",
            local_dir=target_dir,
            local_dir_use_symlinks=False
        )
        print("✅ Chinese RoBERTa downloaded.")
    except Exception as e:
         print(f"❌ Failed to download RoBERTa: {e}")

def download_chinese_hubert():
    print("\n--- Downloading Chinese HuBERT (TencentGameMate/chinese-hubert-base) ---")
    target_dir = os.path.join(BASE_DIR, "chinese-hubert-base")
    ensure_dir(target_dir)
    
    try:
        snapshot_download(
            repo_id="TencentGameMate/chinese-hubert-base",
            local_dir=target_dir,
            local_dir_use_symlinks=False
        )
        print("✅ Chinese HuBERT downloaded.")
    except Exception as e:
        print(f"❌ Failed to download HuBERT: {e}")

if __name__ == "__main__":
    print("Starting Custom Model Download...")
    download_gpt_sovits_base()
    download_chinese_roberta()
    download_chinese_hubert()
    print("\nAll downloads requested.")
