import os
import json
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from groq import Groq

# Configuration & API Key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
MEMORY_FILE = "jarvis_memory.json"

app = Flask("jarvis_cloud_app")
CORS(app)
client = Groq(api_key=GROQ_API_KEY)

def get_active_model():
    try:
        models_data = client.models.list().data
        for m in models_data:
            if any(n in m.id for n in ["qwen", "llama", "gemma", "mixtral"]):
                return m.id
        if models_data:
            return models_data[0].id
    except Exception:
        pass
    return "qwen/qwen2.5-coder-32b-instruct"

ACTIVE_MODEL = get_active_model()

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "user_name": "Endalew",
        "experience": "2 years Price Action trader",
        "discipline_goal": "Stop revenge trading, overcome bad routine, become consistently profitable",
        "channels": "TikTok (Outfit checks & Edits), YouTube (Gaming & Reactions)",
        "trade_logs": []
    }

memory = load_memory()

def ask_ai(user_prompt):
    system_prompt = (
        f"You are Jarvis, Endalew's personal elite Price Action trading mentor, emotional discipline coach, and content co-pilot. "
        f"Endalew has 2 years of trading experience working to overcome bad trading habits and reach profitability. "
        f"He manages TikTok (outfit checks/edits) and YouTube (gaming/reactions). "
        f"Be encouraging, sharp, disciplined, concise, and direct in your responses. Always support Endalew."
    )
    try:
        response = client.chat.completions.create(
            model=ACTIVE_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=350
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Brain Error: {str(e)}"

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
        * { box-sizing: border-box; }
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
        Hello Endalew! I am running 24/7 in the cloud. You can talk to me anytime from your phone, even if your PC is turned off.
    </div>
</div>

<div class="quick-actions">
    <button class="btn-action" onclick="quickCmd('give me a trading discipline rule')">📈 Discipline Rule</button>
    <button class="btn-action" onclick="quickCmd('give me 1 tiktok outfit check idea')">👗 TikTok Outfit</button>
    <button class="btn-action" onclick="quickCmd('give me 1 youtube gaming video hook')">🎮 YouTube Idea</button>
</div>

<div class="input-area">
    <input type="text" id="user-input" placeholder="Ask Jarvis anything..." onkeypress="handleKey(event)">
    <button class="send-btn" onclick="sendMessage()">Send</button>
</div>

<script>
    function addMessage(text, isUser) {
        const container = document.getElementById('chat-container');
        const msgDiv = document.createElement('div');
        msgDiv.className = msg ${isUser ? 'user-msg' : 'jarvis-msg'};
        msgDiv.innerText = text;
        container.appendChild(msgDiv);
        container.scrollTop = container.scrollHeight;
    }

    async function sendMessage() {
        const input = document.getElementById('user-input');
        const text = input.value.trim();
        if (!text) return;

        addMessage(text, true);
        input.value = '';

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            addMessage(data.reply, false);
            
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(data.reply);
                window.speechSynthesis.speak(utterance);
            }
        } catch (e) {
            addMessage("Error connecting to Jarvis server.", false);
        }
    }

    function quickCmd(text) {
        document.getElementById('user-input').value = text;
        sendMessage();
    }

    function handleKey(e) {
        if (e.key === 'Enter') sendMessage();
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
