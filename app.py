from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import langdetect
from langdetect import detect, detect_langs
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

app = FastAPI(
    title="Language Detection API",
    description="An API that detects the language of provided text",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TextInput(BaseModel):
    text: str

class LanguageDetails(BaseModel):
    language: str
    code: str
    probability: float

class LanguageResponse(BaseModel):
    detected_language: str
    language_code: str
    confidence: float
    all_languages: List[LanguageDetails] = []

# Language code to name mapping
LANGUAGE_NAMES = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "et": "Estonian",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "kn": "Kannada",
    "ko": "Korean",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pa": "Punjabi",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "sq": "Albanian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)"
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Language Detection API. Use the /detect endpoint to identify languages."}

@app.get("/health")
def health_check():
    """Health check endpoint for Docker"""
    return {"status": "healthy"}

@app.post("/detect", response_model=LanguageResponse)
def detect_language(text_input: TextInput):
    """
    Detects the language of the provided text.
    
    Returns the detected language with confidence score and alternatives.
    """
    if not text_input.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # For consistent results
        langdetect.DetectorFactory.seed = 0
        
        # Get primary language
        primary_lang_code = detect(text_input.text)
        
        # Get all languages with probabilities
        all_langs = detect_langs(text_input.text)
        
        # Format the response
        primary_lang = all_langs[0]
        lang_name = LANGUAGE_NAMES.get(primary_lang_code, primary_lang_code)
        
        all_languages = [
            LanguageDetails(
                language=LANGUAGE_NAMES.get(lang.lang, lang.lang),
                code=lang.lang,
                probability=round(lang.prob, 4)
            )
            for lang in all_langs
        ]
        
        return LanguageResponse(
            detected_language=lang_name,
            language_code=primary_lang_code,
            confidence=round(primary_lang.prob, 4),
            all_languages=all_languages
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@app.get("/supported-languages")
def get_supported_languages():
    """Returns a list of all supported languages"""
    return {"languages": LANGUAGE_NAMES}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)