from fastapi import FastAPI
import google.generativeai as genai
from groq import Groq
from upstash_redis import Redis

app = FastAPI()

# আপনার Keys (স্ক্রিনশট থেকে সংগৃহীত)
GEMINI_KEY = "AIzaSyCvw8jmBIXxmn1pOd057za1MlneUdgP6w0"
GROQ_KEY = "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"
REDIS_URL = "https://moral-griffon-111737.upstash.io"
REDIS_TOKEN = "gQAAAAAAAbR5AAIgcDlwNjM0ODRjZjhiZGQ0ODQxOTglMDlhYWVlYzRkODUzMw"

genai.configure(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)
redis = Redis(url=REDIS_URL, token=REDIS_TOKEN)

@app.get("/")
def home():
    return {"status": "AI Gateway is Live!"}

@app.get("/ask")
def ask_ai(prompt: str):
    # মেমোরি চেক
    cached = redis.get(prompt)
    if cached:
        return {"response": cached, "source": "memory"}
    try:
        # ডিসিশন লজিক
        if len(prompt) > 80:
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(prompt)
            output = res.text
            source = "gemini"
        else:
            chat = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            output = chat.choices[0].message.content
            source = "groq"
        
        # ১ ঘণ্টার জন্য সেভ রাখা
        redis.set(prompt, output, ex=3600)
        return {"response": output, "source": source}
    except Exception as e:
        return {"error": str(e)}
