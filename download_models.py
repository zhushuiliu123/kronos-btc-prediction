"""测试从 HuggingFace 下载 Kronos-mini 模型"""
import sys
import os

print("Step 1: Testing huggingface_hub download...", flush=True)

try:
    from huggingface_hub import snapshot_download
    print("huggingface_hub imported OK", flush=True)

    cache_dir = os.path.join(os.path.dirname(__file__), "model_cache")
    os.makedirs(cache_dir, exist_ok=True)

    print("Downloading Kronos-Tokenizer-2k...", flush=True)
    tokenizer_path = snapshot_download(
        repo_id="NeoQuasar/Kronos-Tokenizer-2k",
        cache_dir=cache_dir,
        local_files_only=False,
    )
    print(f"Tokenizer downloaded to: {tokenizer_path}", flush=True)

    print("Downloading Kronos-mini...", flush=True)
    model_path = snapshot_download(
        repo_id="NeoQuasar/Kronos-mini",
        cache_dir=cache_dir,
        local_files_only=False,
    )
    print(f"Model downloaded to: {model_path}", flush=True)

    # List files
    print("\nTokenizer files:", flush=True)
    for f in os.listdir(tokenizer_path):
        print(f"  {f}", flush=True)

    print("\nModel files:", flush=True)
    for f in os.listdir(model_path):
        print(f"  {f}", flush=True)

    print("\nAll downloads successful!", flush=True)

except Exception as e:
    print(f"Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
