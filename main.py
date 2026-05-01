from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()

# আপনার Gemini Key
GEMINI_KEY = "AIzaSyCvw8jmBIXxmn1p0d057za1MlneUdgP6w0"
genai.configure(api_key=GEMINI_KEY)

@app.get("/")
def home():
    return {"status": "AI Gateway is Live!"}

@app.get("/ask")
def ask_ai(prompt: str):
    try:
        # সরাসরি Gemini 1.5 Flash ব্যবহার করা হচ্ছে
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(prompt)
        return {"response": res.text, "source": "gemini"}
    except Exception as e:
        return {"error": str(e)}
