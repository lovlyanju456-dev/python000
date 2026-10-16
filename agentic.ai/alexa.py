from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My Alexa Assistant</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #101629, #243b55);
    color: white;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.container {
    width: 100%;
    max-width: 550px;
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 22px;
    box-shadow: 0 15px 45px #0005;
    text-align: center;
}

h1 { color: #55ddff; }

.orb {
    width: 125px;
    height: 125px;
    margin: 25px auto;
    border-radius: 50%;
    background: linear-gradient(135deg, #00d4ff, #7c4dff);
    box-shadow: 0 0 35px #00d4ff88;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 45px;
}

.orb.listening {
    animation: pulse 1s infinite alternate;
}

@keyframes pulse {
    from { transform: scale(1); }
    to { transform: scale(1.12); }
}

input {
    width: 100%;
    padding: 14px;
    border: 0;
    border-radius: 10px;
    font-size: 16px;
    margin: 12px 0;
}

button {
    padding: 12px 18px;
    border: 0;
    border-radius: 10px;
    cursor: pointer;
    font-size: 15px;
    font-weight: bold;
    margin: 5px;
    background: #00d4ff;
    color: #101629;
}

button:hover { opacity: 0.85; }

#response {
    margin-top: 22px;
    padding: 16px;
    min-height: 65px;
    background: #ffffff12;
    border-radius: 12px;
    line-height: 1.6;
    overflow-wrap: anywhere;
}

.small {
    color: #c5d2e5;
    font-size: 13px;
    margin-top: 20px;
}
</style>
</head>

<body>
<div class="container">
    <h1>My Alexa Assistant</h1>
    <p>Your personal Python voice assistant</p>

    <div class="orb" id="orb">🎙️</div>

    <form id="commandForm">
        <input id="command"
               placeholder="Try: hello, time, or how are you"
               autocomplete="off"
               required>
        <button type="submit">Ask Assistant</button>
    </form>

    <button onclick="listen()">🎤 Speak</button>
    <button onclick="stopSpeaking()">🔇 Stop Voice</button>

    <div id="response">Hello! How can I help you today?</div>

    <div class="small">
        Python Flask API · HTML · CSS · JavaScript
    </div>
</div>

<script>
const form = document.getElementById("commandForm");
const input = document.getElementById("command");
const output = document.getElementById("response");
const orb = document.getElementById("orb");

function speak(text) {
    if (!("speechSynthesis" in window)) return;
    speechSynthesis.cancel();
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-IN";
    speechSynthesis.speak(speech);
}

function stopSpeaking() {
    if ("speechSynthesis" in window) speechSynthesis.cancel();
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const command = input.value.trim();
    if (!command) return;

    output.textContent = "Thinking...";

    try {
        const res = await fetch("/api/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({command: command})
        });

        const data = await res.json();
        output.textContent = data.answer;
        speak(data.answer);
    } catch (error) {
        output.textContent = "Could not connect to the Python server.";
    }
});

function listen() {
    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        output.textContent =
            "Voice recognition is not supported in this browser. Try Chrome.";
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.interimResults = false;

    recognition.onstart = () => orb.classList.add("listening");
    recognition.onend = () => orb.classList.remove("listening");

    recognition.onresult = (event) => {
        input.value = event.results[0][0].transcript;
        form.requestSubmit();
    };

    recognition.onerror = () => {
        output.textContent =
            "Microphone error. Allow microphone access and try again.";
    };

    recognition.start();
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    command = str(data.get("command", "")).strip().lower()

    if not command:
        return jsonify({"answer": "Please enter a command."}), 400

    if "hello" in command or "hi" == command:
        answer = "Hello! I am your Python voice assistant."
    elif "how are you" in command:
        answer = "I am doing great! Thanks for asking."
    elif "your name" in command or "who are you" in command:
        answer = "I am your personal Python assistant."
    elif "time" in command:
        from datetime import datetime
        answer = "The current server time is " + datetime.now().strftime("%I:%M %p")
    elif "date" in command or "today" in command:
        from datetime import datetime
        answer = "Today's date is " + datetime.now().strftime("%d %B %Y")
    elif "help" in command or "what can you do" in command:
        answer = (
            "I can greet you, tell you the date and time, "
            "and answer a few basic commands."
        )
    elif "thank" in command:
        answer = "You're welcome! Happy to help."
    elif "bye" in command:
        answer = "Goodbye! Have a wonderful day."
    else:
        answer = (
            "Sorry, I do not know that command yet. "
            "Try hello, how are you, time, date, or help."
        )

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)