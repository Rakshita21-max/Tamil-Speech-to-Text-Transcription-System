import os
import base64
import json
import urllib.request
import urllib.error
import time
import gradio as gr

# Setup HuggingFace TTS API Key from user provided curl
DEFAULT_API_KEY = "AIzaSyBXw9v6UjTEc_PYhZjZcPya_fd3P4HFCl0"

def transcribe(audio_path, api_key, model_name):
    with open("debug_entry.txt", "w", encoding="utf-8") as f:
        f.write(f"Entered transcribe with audio_path: {audio_path}")
        
    if not audio_path:
        return "Please provide an audio recording.", None
    if not api_key:
        return "Please provide a valid API Key.", None

    try:
        # Read the audio file and encode as base64
        with open(audio_path, "rb") as f:
            audio_data = f.read()
        
        base64_audio = base64.b64encode(audio_data).decode("utf-8")
        
        # Determine mime type accurately
        mime_type = "audio/wav"
        lower_path = audio_path.lower()
        if lower_path.endswith(".mp3"):
            mime_type = "audio/mp3"
        elif lower_path.endswith(".ogg"):
            mime_type = "audio/ogg"
        elif lower_path.endswith(".flac"):
            mime_type = "audio/flac"
        elif lower_path.endswith((".m4a", ".aac")):
            mime_type = "audio/aac"
        elif lower_path.endswith(".webm"):
            mime_type = "audio/webm"
        elif lower_path.endswith(".mp4"):
            mime_type = "audio/mp4"

        # Prepare the  API request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key.strip()
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Transcribe the following Tamil speech. Only output the exact Tamil text that is spoken."
                        },
                        {
                            "inlineData": {
                                "mimeType": mime_type,
                                "data": base64_audio
                            }
                        }
                    ]
                }
            ]
        }
        
        # Send request
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    
                    # Parse response
                    if "candidates" in result and len(result["candidates"]) > 0:
                        text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                        
                        # Save to text file for download
                        file_path = "transcription_result.txt"
                        try:
                            with open(file_path, "w", encoding="utf-8") as text_file:
                                text_file.write(text)
                        except Exception as e:
                            print(f"Error saving file: {e}")
                            
                        return text, file_path
                    else:
                        return "No transcription returned. Response: " + str(result), None
            except urllib.error.HTTPError as e:
                try:
                    error_msg = e.read().decode("utf-8", errors="replace")
                except:
                    error_msg = str(e)
                if e.code == 503 and attempt < max_retries - 1:
                    time.sleep(base_delay * (2 ** attempt))
                    continue
                if e.code == 403:
                    return "Authentication Error: The provided API Key is invalid or has been disabled. Please enter a valid API Key.", None
                return f"API Error {e.code}:\n{error_msg}", None
            
    except Exception as e:
        import traceback
        err_str = traceback.format_exc()
        print(f"DEBUG TRANSCRIPTION ERROR: {err_str}")
        try:
            with open("error_log.txt", "w", encoding="utf-8") as f:
                f.write(err_str)
        except Exception as write_err:
            print(f"Failed to write error log: {write_err}")
        
        # Also return Gradio Error so it raises cleanly in the UI
        raise gr.Error(f"Backend Error: {str(e)}")
