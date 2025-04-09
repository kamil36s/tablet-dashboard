from openai import OpenAI
import os
import requests
from datetime import datetime

# Show some debug info
print("🔐 API key starts with:", os.getenv("OPENAI_API_KEY")[:8])
print("🧾 Project ID:", os.getenv("OPENAI_PROJECT_ID"))
print("🟣 Gist ID:", os.getenv("GIST_ID")[:8])

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID")
)

def get_snail_quote():
    prompt = (
        "Write one poetic and mysterious sentence in English about a goth snail "
        "who is a loyal companion and gives comfort through dark times. Avoid clichés."
    )
    print("🔹 Sending prompt to OpenAI...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }]
    )
    quote = response.choices[0].message.content.strip()
    print("✅ Quote:", quote)
    return quote

def update_gist(quote):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"🐌 {quote}\n\n🕒 Updated: {now}"

    url = f"https://api.github.com/gists/{os.getenv('GIST_ID')}"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "files": {
            "message.txt": {
                "content": content
            }
        }
    }

    print("📤 Sending PATCH request to update gist...")
    response = requests.patch(url, headers=headers, json=data)
    print("🔎 Status code:", response.status_code)
    print("🔎 Response:", response.text)
    if response.status_code == 200:
        print("✅ Gist updated successfully.")
    else:
        print("❌ Failed to update gist.")

if __name__ == "__main__":
    print("🚀 Running goth snail quote generator")
    quote = get_snail_quote()
    update_gist(quote)
