let isSubscribed = false;
const subscribeBtn = document.getElementById("subscribeBtn");
const log = document.getElementById('log');

let userId;

if (!localStorage.getItem("userId")) {
    userId = crypto.randomUUID();
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
    const div = document.createElement('div');
    div.textContent = event.data;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
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
    // Log the subscription status
    showVisualNotification("Subscription Status", isSubscribed ? "Subscribed" : "Unsubscribed");
}

function showVisualNotification(title, message) {
    const notif = document.createElement('div');
    notif.textContent = `${title}: ${message}`;
    notif.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: #222;
        color: #fff;
        padding: 10px 20px;
        border-radius: 10px;
        z-index: 9999;
        box-shadow: 0 0 10px #000;
        font-size: 14px;
        font-family: sans-serif;
    `;
    document.body.appendChild(notif);

    setTimeout(() => notif.remove(), 5000);
}