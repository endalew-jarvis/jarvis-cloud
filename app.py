import os
import json
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from groq import Groq

# Получаем ключ из переменных окружения Render
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
MEMORY_FILE = "jarvis_memory.json"

app = Flask("jarvis_cloud_app")
CORS(app)

def get_client():
    if not GROQ_API_KEY:
        return None
    return Groq(api_key=GROQ_API_KEY)

def ask_ai(user_prompt):
    client = get_client()
    if not client:
        return "Jarvis Error: GROQ_API_KEY is not set in Render environment variables."
        
    system_prompt = (
        f"You are Jarvis, Endalew's personal elite Price Action trading mentor, emotional discipline coach, and content co-pilot. "
        f"Endalew has 2 years of trading experience working to overcome bad trading habits and reach profitability. "
        f"He manages TikTok (outfit checks/edits) and YouTube (gaming/reactions). "
        f"Be encouraging, sharp, disciplined, concise, and direct in your responses. Always support Endalew."
    )
    
    models_to_try = ["llama-3.3-70b-versatile", "llama3-8b-8192", "gemma2-9b-it"]
    for model_name in models_to_try:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=350
            )
            return response.choices[0].message.content
        except Exception:
            continue
            
    return "Hello Endalew! I am online. How is your price action chart setup looking right now?"

HTML_INTERFACE = """
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
        }
        header {
            background-color: var(--card-bg);
            border-bottom: 1px solid var(--border);
            padding: 15px 20px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .brand {
            font-size: 1.2rem; font-weight: bold;
            background: linear-gradient(to right, var(--accent-cyan), var(--accent-blue));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .status {
            font-size: 0.75rem; color: #10b981;
            background: rgba(16, 185, 129, 0.1);
            padding: 4px 10px; border-radius: 12px; border: 1px solid #10b981;
        }
        #chat-container {
            flex: 1; overflow-y: auto; padding: 15px;
            display: flex; flex-direction: column; gap: 12px;
        }
        .msg {
            max-width: 85%; padding: 12px 16px; border-radius: 16px;
            font-size: 0.95rem; line-height: 1.5; word-wrap: break-word;
        }
        .user-msg {
            align-self: flex-end; background: #0284c7; color: #fff; border-bottom-right-radius: 4px;
        }
        .jarvis-msg {
            align-self: flex-start; background: var(--card-bg); border: 1px solid var(--border);
color: #e2e8f0; border-bottom-left-radius: 4px;
        }
        .quick-actions {
            display: flex; gap: 8px; padding: 10px 15px; background: #080c14; overflow-x: auto;
        }
        .btn-action {
            background: var(--card-bg); border: 1px solid var(--border);
            color: var(--accent-cyan); padding: 8px 14px; border-radius: 20px;
            font-size: 0.8rem; font-weight: 600; white-space: nowrap; cursor: pointer;
        }
        .input-area {
            display: flex; gap: 8px; padding: 12px 15px;
            background: var(--card-bg); border-top: 1px solid var(--border);
        }
        input[type="text"] {
            flex: 1; background: #030712; border: 1px solid var(--border);
            color: #fff; padding: 12px 16px; border-radius: 24px; font-size: 0.95rem; outline: none;
        }
        button.send-btn {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            border: none; color: #000; font-weight: bold; padding: 0 20px; border-radius: 24px; cursor: pointer;
        }
    </style>
</head>
<body>

<header>
    <div class="brand">🤖 JARVIS 2.0 (24/7 Cloud)</div>
    <div class="status">● Active Cloud</div>
</header>

<div id="chat-container">
    <div class="msg jarvis-msg">
        Hello Endalew! I am running 24/7 in the cloud. I am ready to guide your Price Action trading and content strategy.
    </div>
</div>

<div class="quick-actions">
    <button type="button" class="btn-action" onclick="quickCmd('give me a trading discipline rule')">📈 Discipline Rule</button>
    <button type="button" class="btn-action" onclick="quickCmd('give me 1 tiktok outfit check idea')">👗 TikTok Outfit</button>
    <button type="button" class="btn-action" onclick="quickCmd('give me 1 youtube gaming video hook')">🎮 YouTube Idea</button>
</div>

<div class="input-area">
    <input type="text" id="user-input" placeholder="Ask Jarvis anything..." onkeydown="if(event.key==='Enter') sendMessage();">
    <button type="button" class="send-btn" onclick="sendMessage();">Send</button>
</div>

<script>
    function addMessage(text, isUser) {
        const container = document.getElementById('chat-container');
        const msgDiv = document.createElement('div');
        msgDiv.className = msg ${isUser ? 'user-msg' : 'jarvis-msg'};
        msgDiv.innerText = text;
        container.appendChild(msgDiv);
        container.scrollTop = container.scrollHeight;
        return msgDiv;
    }

    async function sendMessage() {
        const input = document.getElementById('user-input');
        const text = input.value.trim();
        if (!text) return;

        addMessage(text, true);
        input.value = '';

        const loadingDiv = addMessage("Jarvis is thinking...", false);

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            loadingDiv.innerText = data.reply;
            
            if ('speechSynthesis' in window) {
                try {
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(data.reply);
                    utterance.rate = 1.0;
                    window.speechSynthesis.speak(utterance);
                } catch(e) {}
            }
        } catch (e) {
            loadingDiv.innerText = "Jarvis Cloud active! What trade setup are we analyzing today?";
        }
    }

    function quickCmd(text) {
        document.getElementById('user-input').value = text;
        sendMessage();
    }
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_msg = data.get("message", "")
    reply = ask_ai(user_msg)
    return jsonify({"reply": reply})
if name == 'main':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
