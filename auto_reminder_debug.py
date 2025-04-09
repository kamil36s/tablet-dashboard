
import openai
import requests
import os
from datetime import datetime

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "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"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or "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"
GIST_ID = "c360e04023681671edeb14d4a80a2369"
GIST_FILENAME = "message.txt"

openai.api_key = OPENAI_API_KEY

prompty = {
    "morning": "Napisz motywującą wiadomość na poranek dla osoby z ADHD i lekką depresją, maksymalnie 1 zdanie.",
    "afternoon": "Napisz krótkie przypomnienie w stylu: 'czas na wodę, spacer, przerwę'. Maksymalnie jedno zdanie.",
    "evening": "Napisz ciepłą wiadomość na wieczór, spokojną i wyciszającą. Jedno zdanie."
}

def get_message(prompt):
    print(f"🔹 Prompt: {prompt}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }]
    )
    message = response.choices[0].message.content.strip()
    print(f"✅ Generated message: {message}")
    return message

def generate_reminders():
    print("🟡 Generating all reminders...")
    return {
        "morning": get_message(prompty["morning"]),
        "afternoon": get_message(prompty["afternoon"]),
        "evening": get_message(prompty["evening"])
    }

def update_gist(content):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "files": {
            GIST_FILENAME: {
                "content": content
            }
        }
    }
    print("🟡 Sending PATCH request to GitHub Gist API...")
    print("➡️ URL:", url)
    print("➡️ Headers:", headers)
    print("➡️ Data:", data)

    response = requests.patch(url, json=data, headers=headers)
    print("🔎 Response status code:", response.status_code)
    print("🔎 Response text:", response.text)
    if response.status_code == 200:
        print("✅ Gist successfully updated.")
    else:
        print("❌ Failed to update Gist.")

if __name__ == "__main__":
    print("🚀 Running debug auto_reminder script")
    now = datetime.now().hour
    reminders = generate_reminders()

    full_message = f"☀️ {reminders['morning']}\n\n🌤 {reminders['afternoon']}\n\n🌙 {reminders['evening']}"
    print("📄 Full message to upload:")
    print(full_message)

    update_gist(full_message)
