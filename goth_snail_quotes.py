from openai import OpenAI
import os
from datetime import datetime

print("🔐 API key starts with:", os.getenv("OPENAI_API_KEY")[:8])
print("🧾 Project ID:", os.getenv("OPENAI_PROJECT_ID"))

# Initialize client using environment variables
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

def update_message_file(quote):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"🐌 {quote}\n\n🕒 Updated: {now}"
    with open("message.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ message.txt updated")

if __name__ == "__main__":
    print("🚀 Running goth snail quote generator")
    quote = get_snail_quote()
    update_message_file(quote)
