const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

async function askAI() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    userInput.value = '';

    const tempMsg = addMessage("Analyzing ERP data...", 'bot');

    try {
        // Ensure the URL is exactly http://127.0.0.1:8000/chat
        const res = await fetch(`http://127.0.0.1:8000/chat?query=${encodeURIComponent(text)}`);
        // FIX: Ensure you use 'res' here, not 'response'
        const data = await res.json();
        tempMsg.innerHTML = data.response;
    } catch (err) {
        console.error(err); // This helps you see the REAL error in F12 Console
        tempMsg.innerHTML = "❌ Connection Error. Is the FastAPI server running?";
    }
}

function addMessage(text, type) {
    const div = document.createElement('div');
    div.className = `msg ${type}`;
    div.innerHTML = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return div;
}

sendBtn.addEventListener('click', askAI);
userInput.addEventListener('keypress', (e) => { if(e.key === 'Enter') askAI(); });
