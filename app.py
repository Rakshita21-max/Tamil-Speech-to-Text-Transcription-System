import os
import base64
import json
import urllib.request
import urllib.error
import time
import gradio as gr

# Setup API Key from user provided curl
DEFAULT_API_KEY = "*****************************************"

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

custom_css = """
.theme-switch-wrapper {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 10px;
}
.theme-switch {
  position: relative;
  display: inline-block;
  width: 140px;
  height: 50px;
}
.theme-switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e6e9ef;
  transition: .4s;
  border-radius: 50px;
  box-shadow: inset 5px 5px 10px #c8cdd4, inset -5px -5px 10px #ffffff;
  display: flex;
  align-items: center;
  overflow: hidden;
}
.mode-text {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: 700;
  font-size: 13px;
  position: absolute;
  z-index: 1;
  transition: .4s;
}
.light-text {
  right: 15px;
  color: #929aab;
}
.dark-text {
  left: 15px;
  color: #8b92a5;
  opacity: 0;
}
.icon-container {
  position: absolute;
  height: 40px;
  width: 40px;
  left: 5px;
  bottom: 5px;
  background-color: #f0f3f8;
  border-radius: 50%;
  transition: .4s;
  box-shadow: 4px 4px 8px #c8cdd4, -4px -4px 8px #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  color: #929aab;
}
.moon-icon {
  display: none;
}
/* Dark Mode Styles triggered by the checkbox */
input:checked + .slider {
  background-color: #2a2d3c;
  box-shadow: inset 5px 5px 10px #1e202a, inset -5px -5px 10px #363a4e;
}
input:checked + .slider .light-text {
  opacity: 0;
}
input:checked + .slider .dark-text {
  opacity: 1;
  color: #8b92a5;
}
input:checked + .slider .icon-container {
  transform: translateX(90px);
  background-color: #7b819f; 
  box-shadow: 4px 4px 8px #1e202a, -4px -4px 8px #363a4e;
  color: #ffffff; 
}
input:checked + .slider .sun-icon {
  display: none;
}
input:checked + .slider .moon-icon {
  display: block;
}
"""

html_switch = """    #theme of dark and light switch method of web page
<div class="theme-switch-wrapper">
  <label class="theme-switch" for="theme-checkbox">
    <input type="checkbox" id="theme-checkbox" onchange="
      var isDark = this.checked;
      var html = document.documentElement;
      var body = document.body;
      var app = document.querySelector('gradio-app');
      
      if (isDark) {
         body.classList.add('dark');
         html.classList.add('dark');
         if(app) app.classList.add('dark');
      } else {
         body.classList.remove('dark');
         html.classList.remove('dark');
         if(app) app.classList.remove('dark');
      }
    " />
    <div class="slider round">
      <span class="mode-text light-text">LIGHT MODE</span>
      <span class="mode-text dark-text">DARK MODE</span>
      <div class="icon-container">
        <!-- Sun Icon -->
        <svg class="sun-icon" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>
        <!-- Moon Icon -->
        <svg class="moon-icon" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
      </div>
    </div>
  </label>
</div>
<script>
  setTimeout(function() {
      var isDark = document.body.classList.contains('dark') || 
                   document.documentElement.classList.contains('dark') || 
                   (document.querySelector('gradio-app') && document.querySelector('gradio-app').classList.contains('dark'));
      var cb = document.getElementById('theme-checkbox');
      if(cb && isDark) { cb.checked = true; }
  }, 500);
</script>
"""

# Define the Gradio interface
with gr.Blocks(title="Tamil Speech-to-Text", theme=gr.themes.Soft(), css=custom_css) as demo:
    with gr.Row():
        with gr.Column(scale=4):
            gr.Markdown("# 🎙️ Tamil Speech-to-Text Transcription System")
            gr.Markdown("Record your voice or upload an audio file to convert Tamil speech into text quickly and accurately.")
        with gr.Column(scale=1, min_width=150):
            theme_btn = gr.HTML(html_switch)
            
    with gr.Row():
        with gr.Column(scale=1):
            api_key_input = gr.Textbox(
                label="Gemini API Key", 
                type="password", 
                value=DEFAULT_API_KEY,
                visible=False
            )
            model_input = gr.Textbox(
                label="Model Name", 
                value="gemini-flash-latest",
                visible=False
            )
            
            with gr.Tabs():
                with gr.Tab("🎤 Record"):
                    audio_mic = gr.Audio(sources=["microphone"], type="filepath", label="Mic Input", format="wav")
                    btn_mic = gr.Button("Transcribe Recording", variant="primary")
                with gr.Tab("📁 Upload"):
                    audio_upload = gr.Audio(sources=["upload"], type="filepath", label="File Input", format="wav")
                    btn_upload = gr.Button("Transcribe File", variant="primary")
                    
        with gr.Column(scale=1):
            text_output = gr.Textbox(label="Transcription Result", lines=12, placeholder="Transcription will appear here...")
            file_output = gr.File(label="Download Transcription as TXT")
            
    # Map both buttons to the same transcribe function and output
    btn_mic.click(fn=transcribe, inputs=[audio_mic, api_key_input, model_input], outputs=[text_output, file_output])
    btn_upload.click(fn=transcribe, inputs=[audio_upload, api_key_input, model_input], outputs=[text_output, file_output])
def get_free_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

if __name__ == "__main__":
    free_port = get_free_port()
    print(f"--- DEBUG: Starting Gradio on port {free_port} ---")
    demo.launch(
        server_name="127.0.0.1", 
        server_port=free_port,
        share=False,
        inbrowser=True,
        show_api=False
    )
