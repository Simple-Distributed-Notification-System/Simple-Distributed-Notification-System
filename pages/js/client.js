let isSubscribed = false;
const subscribeBtn = document.getElementById("subscribeBtn");
const log = document.getElementById('log');

// Generate a random user ID between user0 and user999999
const userId = 'user' + Math.floor(Math.random() * 1000000);
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

    const div = document.createElement('div');
    div.textContent = isSubscribed ? "✅ Subscribed" : "❌ Unsubscribed";
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
}