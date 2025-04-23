let isSubscribed = false;
let userId = "";
const subscribeBtn = document.getElementById("subscribeBtn");
const log = document.getElementById('log');

if (!localStorage.getItem("userId")) {
    userId = uuidv4();
    localStorage.setItem("userId", userId);
} else {
    userId = localStorage.getItem("userId");
}


const ws = new WebSocket(`wss://${location.host}/ws/client/${userId}`);

ws.onopen = function() {
    console.log("userId:", userId);
    console.log("WebSocket connection established.");
};

ws.onmessage = function(event) {
    const msg = JSON.parse(event.data);

    if (msg.type === "notification") {
        displayMassage(msg.message);
    }
};

ws.onerror = function(error) {
    console.log("WebSocket error:", error);
};

ws.onclose = function(event) {
    console.log("WebSocket closed:", event);
    console.log("Close code:", event.code, "Reason:", event.reason);

    showVisualNotification("Connection closed (" + event.code + ")", event.reason);
};

function subscription() {
    if (ws.readyState === WebSocket.OPEN) {
        isSubscribed = !isSubscribed;
        subscribeBtn.innerText = isSubscribed ? "Unsubscribe" : "Subscribe";
        ws.send(isSubscribed ? "subscribe" : "unsubscribe");

        showVisualNotification("Subscription Status", isSubscribed ? "Subscribed" : "Unsubscribed");
    } else {
        showVisualNotification("Error", "Not connected to server");
    }
}

function showVisualNotification(title, message) {
    const notify = document.createElement('div');
    notify.textContent = `${title}: ${message}`;
    notify.classList.add('notification');
    document.body.appendChild(notify);

    setTimeout(() => notify.remove(), 5000);
}

function displayMassage(msg) {
    const messageCard = document.createElement('div');
    messageCard.className = 'message-card fade-in';

    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = msg;

    messageCard.appendChild(messageText);
    log.appendChild(messageCard);
    log.scrollTop = log.scrollHeight;
}
