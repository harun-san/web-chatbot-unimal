// Konfigurasi URL API Backend (Hugging Face / Local)
const API_URL = "http://localhost:7860/api/chat";

// Ambil elemen DOM
const fabBtn = document.getElementById('fabBtn');
const chatWidget = document.getElementById('chatWidget');
const closeChatBtn = document.getElementById('closeChatBtn');
const chatBody = document.getElementById('chatBody');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const mainNav = document.getElementById('mainNav');

// --- Efek UI: Navbar Scrolled Background ---
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        mainNav.style.backgroundColor = "rgba(0, 77, 64, 0.95)";
        mainNav.style.backdropFilter = "blur(10px)";
    } else {
        mainNav.style.backgroundColor = "#004d40";
        mainNav.style.backdropFilter = "none";
    }
});

// --- Event Listener Buka/Tutup Chatbox ---
fabBtn.addEventListener('click', () => {
    chatWidget.classList.add('active');
    // Beri sedikit waktu untuk animasi, lalu fokuskan kursor ke input
    setTimeout(() => chatInput.focus(), 300);
});

closeChatBtn.addEventListener('click', () => {
    chatWidget.classList.remove('active');
});

// --- Logika Chatbot Backend ---
function scrollToBottom() {
    chatBody.scrollTop = chatBody.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault(); // Mencegah spasi ganda bawaan browser
        sendMessage();
    }
});

async function sendMessage() {
    const text = chatInput.value.trim();
    if (text === "") return;

    // 1. Tampilkan Pesan User
    appendMessage(text, 'user-message');
    chatInput.value = '';
    
    // 2. Tampilkan Indikator "Mengetik..."
    const typingId = "typing-" + Date.now();
    appendTypingIndicator(typingId);

    try {
        // 3. Panggil API Backend
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // 4. Hapus Indikator & Tampilkan Respons
        removeElement(typingId);
        appendMessage(data.response, 'bot-message');

    } catch (error) {
        console.error("Error memanggil API:", error);
        removeElement(typingId);
        appendMessage("Maaf, sepertinya jaringan terputus atau server sedang tidur. Silakan coba lagi nanti.", 'bot-message');
    }
}

// --- Fungsi Bantuan Pembuat Elemen UI ---
function appendMessage(text, className) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className} shadow-sm`;
    msgDiv.textContent = text;
    chatBody.appendChild(msgDiv);
    scrollToBottom();
}

function appendTypingIndicator(id) {
    const typingDiv = document.createElement('div');
    typingDiv.id = id;
    typingDiv.className = "typing-indicator";
    typingDiv.innerHTML = `<i class="bi bi-three-dots text-success fs-4"></i>`;
    chatBody.appendChild(typingDiv);
    scrollToBottom();
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) {
        el.remove();
    }
}