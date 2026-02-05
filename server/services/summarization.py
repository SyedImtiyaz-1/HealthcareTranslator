import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

async def generate_summary(messages: list) -> str:
    if not messages:
        return "No messages to summarize."
    
    conversation_text = ""
    for msg in messages:
        role = msg.get("role", "unknown").upper()
        text = msg.get("original_text", "") or msg.get("translated_text", "")
        if text:
            conversation_text += f"{role}: {text}\n"
    
    if not conversation_text.strip():
        return "No text content to summarize."
    
    prompt = f"""Analyze the following doctor-patient conversation and provide a structured medical summary.

CONVERSATION:
{conversation_text}

Provide a summary with the following sections (only include sections that have relevant information):

1. CHIEF COMPLAINT: Main reason for the visit
2. SYMPTOMS: List of reported symptoms
3. DIAGNOSIS: Any diagnoses mentioned
4. MEDICATIONS: Prescribed or discussed medications
5. TREATMENT PLAN: Recommended treatments or procedures
6. FOLLOW-UP: Next steps or follow-up instructions

Keep the summary concise and professional. Use bullet points where appropriate."""

    try:
        # Use Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = await model.generate_content_async(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Gemini returned an empty response."
            
    except Exception as e:
        print(f"Summarization error (Gemini): {e}")
        return f"Unable to generate summary. Error: {str(e)}"
