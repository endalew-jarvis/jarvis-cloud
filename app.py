import os
import json
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from groq import Groq

# Получаем данные из настроек Render
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

app = Flask("jarvis_app")
CORS(app)

def ask_ai(user_prompt):
    client = Groq(api_key=GROQ_API_KEY)
    system_prompt = "You are Jarvis, Endalew's personal elite Price Action trading mentor and content co-pilot. Be sharp, disciplined, and concise."
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Brain Error: {str(e)}"

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>JARVIS 2.0</title>
    <style>
        body { background: #0b0f19; color: #fff; font-family: sans-serif; padding: 20px; text-align: center; }
        input { width: 90%; padding: 15px; border-radius: 20px; background: #1e293b; color: #fff; border: 1px solid #334155; }
        button { padding: 15px 30px; border-radius: 20px; background: #22d3ee; color: #000; font-weight: bold; margin-top: 15px; cursor: pointer; }
        #reply { margin-top: 20px; padding: 15px; background: #161f30; border-radius: 12px; }
    </style>
    </head>
    <body>
        <h1>🤖 JARVIS 2.0</h1>
        <input type="text" id="msg" placeholder="Ask Jarvis anything...">
        <br><button onclick="send()">Send</button>
        <div id="reply">Waiting for input...</div>
        <script>
            async function send() {
                const text = document.getElementById('msg').value;
                document.getElementById('reply').innerText = "Jarvis is thinking...";
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                document.getElementById('reply').innerText = data.reply;
            }
        </script>
    </body>
    </html>
    """)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    return jsonify({"reply": ask_ai(data.get("message", ""))})

# Запуск приложения
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
