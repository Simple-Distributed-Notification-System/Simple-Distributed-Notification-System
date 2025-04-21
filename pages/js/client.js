let isSubscribed = false;
let userId = null;
const subscribeBtn = document.getElementById("subscribeBtn");
const log = document.getElementById('log');

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

if (!localStorage.getItem("userId")) {
    userId = generateUUID();
    localStorage.setItem("userId", userId);
} else {
    userId = localStorage.getItem("userId");
}

const ws = new WebSocket(`ws://${location.host}/ws/client/${userId}`);

ws.onopen = function() {
    console.log("userId:", userId);
    console.log("WebSocket connection established.");
};

ws.onmessage = function(event) {
    const msg = JSON.parse(event.data);

    if (msg.type === "notification") {
        const messageCard = document.createElement('div');
        messageCard.className = 'message-card fade-in';

        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = msg.message;

        messageCard.appendChild(messageText);
        log.appendChild(messageCard);
        log.scrollTop = log.scrollHeight;
    }
};

ws.onerror = function(error) {
    console.log("WebSocket error:", error);
};

ws.onclose = function(event) {
    console.log("WebSocket closed:", event);
};

function subscription() {
    isSubscribed = !isSubscribed;
    subscribeBtn.innerText = isSubscribed ? "Unsubscribe" : "Subscribe";
    ws.send(isSubscribed ? "subscribe" : "unsubscribe");

    showVisualNotification("Subscription Status", isSubscribed ? "Subscribed" : "Unsubscribed");
}

function showVisualNotification(title, message) {
    const notify = document.createElement('div');
    notify.textContent = `${title}: ${message}`;
    notify.classList.add('notification');
    document.body.appendChild(notify);

    setTimeout(() => notify.remove(), 5000);
}