import os
import requests
from flask import Flask, render_template_string, request, jsonify, send_file
from flask_cors import CORS
from groq import Groq
import io

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")

# ID британского глубокого мужского голоса (Jarvis style)
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb" 

app = Flask("jarvis_cloud_app")
CORS(app)

def ask_ai(user_prompt):
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        return f"Client Error: {str(e)}"
        
    # ПРЯМАЯ ИНСТРУКЦИЯ: Никаких размышлений и списков анализа!
    system_prompt = (
        "You are JARVIS, Endalew's personal elite Price Action trading mentor, emotional discipline coach, and content co-pilot. "
        "CRITICAL INSTRUCTION: Respond directly as JARVIS. DO NOT include any internal analysis, CoT, reasoning steps, or headings like '1. Analyze User Input'. "
        "Output ONLY the final conversational response. Be sharp, disciplined, encouraging, and concise."
    )
    
    preferred_models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "llama3-8b-8192"]
    
    for model_name in preferred_models:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.6
            )
            reply = response.choices[0].message.content.strip()
            return reply
        except Exception:
            continue
            
    return "Protocol active, Endalew. Systems ready. State your objective."

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>JARVIS 2.0 Assistant</title>
        <style>
            :root {
                --bg-dark: #0b0f19;
                --card-bg: #131d31;
                --accent-blue: #38bdf8;
                --accent-cyan: #22d3ee;
                --text-main: #f8fafc;
                --border: #1e293b;
            }
            * { box-sizing: border-box; touch-action: manipulation; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: var(--bg-dark);
                color: var(--text-main);
                margin: 0; padding: 0;
                display: flex; flex-direction: column; height: 100vh;
                text-align: center;
            }
            header {
                background-color: var(--card-bg);
                border-bottom: 1px solid var(--border);
                padding: 15px 20px;
            }
            .brand {
                font-size: 1.4rem; font-weight: bold;
                background: linear-gradient(to right, var(--accent-cyan), var(--accent-blue));
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            }
            .container {
                flex: 1; padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center;
            }
            input[type="text"] {
                width: 90%; max-width: 400px; background: #030712; border: 1px solid var(--border);
                color: #fff; padding: 15px 20px; border-radius: 24px; font-size: 1rem; outline: none; margin-bottom: 15px;
            }
            button {
                background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
border: none; color: #000; font-weight: bold; padding: 12px 36px; border-radius: 24px; font-size: 1rem; cursor: pointer;
            }
            #reply {
                margin-top: 25px; width: 90%; max-width: 450px; background: var(--card-bg);
                border: 1px solid var(--border); padding: 18px; border-radius: 16px;
                font-size: 1rem; line-height: 1.5; color: #38bdf8; text-align: left;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="brand">🤖 JARVIS 2.0 (Movie Audio)</div>
        </header>

        <div class="container">
            <input type="text" id="msg" placeholder="Ask Jarvis anything..." onkeydown="if(event.key==='Enter') send();">
            <button onclick="send()">Send Command</button>
            <div id="reply">Hello Endalew! Systems active. ElevenLabs voice module ready.</div>
        </div>

        <script>
            async function send() {
                const input = document.getElementById('msg');
                const text = input.value.trim();
                if(!text) return;
                
                const replyDiv = document.getElementById('reply');
                replyDiv.innerText = "Jarvis processing...";
                input.value = '';

                try {
                    const res = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: text})
                    });
                    const data = await res.json();
                    replyDiv.innerText = data.reply;
                    
                    // Речевой вывод через синтез речи
                    if ('speechSynthesis' in window) {
                        try {
                            window.speechSynthesis.cancel();
                            const utterance = new SpeechSynthesisUtterance(data.reply);
                            utterance.rate = 0.95;
                            utterance.pitch = 0.9;
                            window.speechSynthesis.speak(utterance);
                        } catch(e) {}
                    }
                } catch(e) {
                    replyDiv.innerText = "Connection error to Jarvis Cloud.";
                }
            }
        </script>
    </body>
    </html>
    """)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    msg = data.get("message", "")
    reply = ask_ai(msg)
    return jsonify({"reply": reply})

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
