from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()

# আপনার দেওয়া নতুন Gemini Key
GEMINI_KEY = "AIzaSyBpK2CYVMH_i5leVnrCh0K-LYE-qDJZN4U"
genai.configure(api_key=GEMINI_KEY)

@app.get("/")
def home():
    return {"status": "AI Gateway is Live!"}

@app.get("/ask")
def ask_ai(prompt: str):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(prompt)
        return {"response": res.text, "source": "gemini"}
    except Exception as e:
        return {"error": str(e)}
