import os
from deep_translator import GoogleTranslator

# simple cache to avoid re-translating same text
translation_cache = {}

async def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    if not text or not text.strip():
        return ""
    
    if source_lang == target_lang:
        return text
    
    # Cache key
    key = f"{text}_{source_lang}_{target_lang}"
    if key in translation_cache:
        return translation_cache[key]
    
    try:
        # Use deep_translator
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text)
        
        translation_cache[key] = translated
        return translated
                
    except Exception as e:
        print(f"Translation error: {e}")
        return text


SUPPORTED_LANGUAGES = [
    {"code": "en", "name": "English"},
    {"code": "es", "name": "Spanish"},
    {"code": "fr", "name": "French"},
    {"code": "de", "name": "German"},
    {"code": "it", "name": "Italian"},
    {"code": "pt", "name": "Portuguese"},
    {"code": "ru", "name": "Russian"},
    {"code": "zh-CN", "name": "Chinese"}, # deep_translator uses zh-CN
    {"code": "ja", "name": "Japanese"},
    {"code": "ko", "name": "Korean"},
    {"code": "ar", "name": "Arabic"},
    {"code": "hi", "name": "Hindi"},
]
