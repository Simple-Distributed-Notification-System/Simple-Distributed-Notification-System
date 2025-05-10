let isSubscribed = false;
let userId = "";
let notificationCount = 0;
const subscribeBtn = document.getElementById("subscribeBtn");
const log = document.getElementById('log');
const modal = document.getElementById("loginModal");
const loginBtn = document.getElementById("loginBtn");
const submitLoginBtn = document.getElementById("submitLoginBtn");
const cancelLoginBtn = document.getElementById("cancelLoginBtn");
const span = document.getElementsByClassName("close")[0];

// Remove trailing slash from WebSocket URL
const ws = new WebSocket(`wss://${location.host}/ws/client`);

ws.onopen = function() {
    console.log("WebSocket connection established.");
    showVisualNotification("Connection", "Connected to server");
    if (localStorage.getItem("userId")) {
        userId = localStorage.getItem("userId");
        ws.send(JSON.stringify({
            action: "userId",
            userId: userId
        }));
    }
};

ws.onmessage = function(event) {
    const msg = JSON.parse(event.data);

    if (msg.type === "notification") {
        displayMessage(msg.message);
    }
    if (msg.type === "success" && msg.msg) {
        log.innerHTML = "";
        msg.msg.forEach(notification => {
            displayMessage(notification);
        });
    }
    if (msg.isSubscribed != undefined && msg.type === "success") {
        if (msg.isSubscribed !== undefined) {
            isSubscribed = msg.isSubscribed;
            subscribeBtn.innerText = isSubscribed ? "Unsubscribe" : "Subscribe";
            showVisualNotification("Subscription Status", isSubscribed ? "Subscribed" : "Unsubscribed");
        }
    } else if (msg.type === "success") {
        showVisualNotification("Success", msg.message);
        if (msg.userId) {
            userId = msg.userId;
        }
    }

    if (msg.type === "error") {
        console.log("Error:", msg.message);
        showVisualNotification("Error", msg.message);
    }
    if (msg.type === "error_email") {
        console.log("Email Error:", msg.message);
        showVisualNotification("Email Error", msg.message);
    }
    if (msg.type === "error_token") {
        console.log("Token Error:", msg.message);
        showVisualNotification("Token Error", msg.message);
    }
};

ws.onerror = function(error) {
    console.log("WebSocket error:", error);
    showVisualNotification("Connection Error", "Failed to connect to server");
};

ws.onclose = function(event) {
    console.log("WebSocket closed:", event);
    console.log("Close code:", event.code, "Reason:", event.reason);

    showVisualNotification("Connection closed (" + event.code + ")", event.reason || "Connection lost");
};

function login() {
    if (ws.readyState === WebSocket.OPEN) {
        const email = document.getElementById('emailInput').value.trim();
        if (email) {
            ws.send(JSON.stringify({
                action: "login",
                email: email.toLowerCase()
            }));
            showVisualNotification("Login", email);
        } else {
            showVisualNotification("Error", "Please enter an email address");
        }
    } else {
        showVisualNotification("Error", "Not connected to server");
    }
}

function subscription() {
    if (ws.readyState === WebSocket.OPEN) {
        isSubscribed = !isSubscribed;
        ws.send(JSON.stringify({
            action: isSubscribed ? "subscribe" : "unsubscribe",
            userId: userId
        }));
    } else {
        showVisualNotification("Error", "Not connected to server");
    }
}

function showVisualNotification(title, message) {
    const notify = document.createElement('div');
    notify.textContent = `${title}: ${message}`;
    notify.classList.add('notification');
    
    // Dynamically position the notification based on the count
    notify.style.top = `${20 + notificationCount * 70}px`;  // Adjust 70px based on your notification height
    
    document.body.appendChild(notify);
    notificationCount++; // Increment the notification count

    setTimeout(() => {
        notify.remove();
        notificationCount--; // Decrement the count when removed
        // Reposition other notifications
        const notifications = document.querySelectorAll('.notification');
        notifications.forEach((notif, index) => {
            notif.style.top = `${20 + index * 70}px`;
        });
    }, 5000); // Remove after 5 seconds
}

function displayMessage(msg) {
    const messageCard = document.createElement('div');
    messageCard.className = 'message-card fade-in';

    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = msg;

    messageCard.appendChild(messageText);
    log.appendChild(messageCard);
    log.scrollTop = log.scrollHeight;
}

// Open modal when clicking login button
loginBtn.addEventListener("click", function() {
    modal.style.display = "block";
});

// Close modal with X button
span.addEventListener("click", function() {
    modal.style.display = "none";
});

// Close modal with Cancel button
cancelLoginBtn.addEventListener("click", function() {
    modal.style.display = "none";
});

// Submit login
submitLoginBtn.addEventListener("click", function() {
    login();
    modal.style.display = "none";
});

// Close modal when clicking outside
window.addEventListener("click", function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
});

// Allow Enter key to submit the form
document.getElementById("emailInput").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        login();
        modal.style.display = "none";
    }
});