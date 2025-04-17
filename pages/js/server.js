const log = document.getElementById('messages');
const countSubscribers = document.getElementById("count-subscribers");
const countClients = document.getElementById("count-clients");
const ws = new WebSocket(`ws://${location.host}/ws/server`);

// Wait for the WebSocket to open
ws.onopen = () => {
    console.log("WebSocket connection established");
    // Send the count request when the connection is open
    ws.send(JSON.stringify({ action: "count" }));
};

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data); // Parse the message to an object

    if (msg.type === "counts") {
        countSubscribers.textContent = msg.subscribers;
        countClients.textContent = msg.clients;
    }
};

function send() {
    const msg = document.getElementById("msg").value.trim();
    if (!msg) return alert("Message is empty!");

    const div = document.createElement("div");
    div.textContent = msg;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;

    // Send message only if WebSocket is open
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: "notify", message: msg }));
    } else {
        alert("WebSocket is not open yet!");
    }
}

// IF RELOADING THE PAGE, CHECK IF THE USER IS SUBSCRIBED
window.onload = function() {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: "count" }));
    } else {
        ws.onopen = () => ws.send(JSON.stringify({ action: "count" }));
    }
};
