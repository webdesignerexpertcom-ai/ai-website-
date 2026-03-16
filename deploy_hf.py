from huggingface_hub import HfApi
import os

# Read token from secrets.toml
token = ""
secrets_path = os.path.join(".streamlit", "secrets.toml")
if os.path.exists(secrets_path):
    with open(secrets_path, "r") as f:
        for line in f:
            if "HF_TOKEN" in line:
                token = line.split("=")[1].strip().strip('"')

if not token:
    print("Error: HF_TOKEN not found in .streamlit/secrets.toml")
    exit(1)

api = HfApi(token=token)

repo_id = "bhanu131/ai-website-generator"

# Create the Space with docker SDK (for Streamlit)
try:
    api.create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="docker",
        private=False,
        exist_ok=True
    )
    print(f"Space created: https://huggingface.co/spaces/{repo_id}")
except Exception as e:
    print(f"Space creation note: {e}")

# Upload the entire folder
api.upload_folder(
    folder_path=".",
    repo_id=repo_id,
    repo_type="space",
    ignore_patterns=[".git*", ".streamlit*", "__pycache__*", "*.pyc", "deploy_hf.py"]
)

print("Done! Visit: https://huggingface.co/spaces/" + repo_id)
