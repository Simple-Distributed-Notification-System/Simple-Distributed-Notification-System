const log = document.getElementById('messages');
const countSubscribers = document.getElementById("count-subscribers");
const countClients = document.getElementById("count-clients");
const countClientsOnline = document.getElementById("count-clients-online");
const countSubscribersOnline = document.getElementById("count-subscribers-online");

// Check if counts have been requested after reconnect
let countsRequested = false;
// Store the full notification data including subscribers
let notificationsData = [];
// Store the current notification being viewed in popup
let currentViewedNotification = null;

// Connect to WebSocket
const ws = new WebSocket(`wss://${location.host}/ws/server`);

ws.onopen = () => {
    console.log("WebSocket connection established");

    if (!countsRequested) {
        sendCount();
    }
};

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "counts") {
        countSubscribersOnline.textContent = msg.subscribersOnline;
        countClientsOnline.textContent = msg.online;
        countClients.textContent = msg.clients;
        countSubscribers.textContent = msg.allSubscribers;
    }

    if (msg.type === "notifications") {
        log.innerHTML = "";
        notificationsData = msg.notifications; // Store notifications data
        msg.notifications.forEach(notification => {
            displayMessage(notification);
        });
    }
    
    if (msg.type === "users") {
        // Update user data 
        const popup = document.getElementById('popup');
        updateUserList(msg.users, msg.notificationId);

        // If popup is open, keep the display updated
        if (!popup.classList.contains('hidden')) {
        }
    }

    // Handle real-time notification updates
    if (msg.type === "notification_update") {
        if (currentViewedNotification === msg.notificationId) {
            requestUserData(msg.notificationId);
        }
    }
};    

ws.onerror = (error) => {
    console.error("WebSocket error:", error);
};

ws.onclose = () => {
    console.warn("WebSocket connection closed");
};

function send() {
    if (countSubscribers.textContent === "0") {
        return alert("No subscribers to notify!");
    }

    const msgInput = document.getElementById("msg");
    const msg = msgInput.value;
    if (!msg) return alert("Message is empty!");

    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: "notify", message: msg }));
        message = {
            "message": msg,
            "timestamp": new Date().toISOString()
        }
        location.reload();

        msgInput.value = "";
    } else {
        alert("WebSocket is not open yet!");
    }
}

// Re-send count request after reload once WebSocket is open
window.addEventListener("load", () => {
    if (ws.readyState === WebSocket.OPEN) {
        sendCount();
    } else {
        ws.addEventListener("open", () => {
            if (!countsRequested) {
                sendCount();
            }
        });
    }
});

// function to send count
function sendCount() {
    ws.send(JSON.stringify({ action: "count" }));
    ws.send(JSON.stringify({ action: "get_notifications" }));
    countsRequested = true;
}

function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function formatDateTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

function displayMessage(msg) {
    const messageCard = document.createElement('div');
    messageCard.className = 'message-card fade-in';
    
    const cardContent = document.createElement('div');
    cardContent.className = 'message-card-content';

    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = msg.message;

    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = formatTime(msg.timestamp);

    cardContent.appendChild(messageText);
    cardContent.appendChild(messageTime);
    messageCard.appendChild(cardContent);
    log.appendChild(messageCard);
    log.scrollTop = log.scrollHeight;

    // Add notification ID as data 
    if (msg._id) {
        messageCard.dataset.notificationId = msg._id;
    }

    messageCard.addEventListener('click', () => {
        const notificationId = messageCard.dataset.notificationId;
        document.querySelector('.popup-message').textContent = msg.message;
        document.querySelector('.popup-time').textContent = formatDateTime(msg.timestamp);
        
        // Clear previous user lists
        document.getElementById('seen-users').innerHTML = '';
        document.getElementById('unseen-users').innerHTML = '';
        
        // Show popup
        document.getElementById('popup').classList.remove('hidden');
        
        // Store current viewed notification ID
        currentViewedNotification = notificationId;
        
        // Request user data for this notification
        if (notificationId) {
            requestUserData(notificationId);
        }
    });
}

function requestUserData(notificationId) {
    ws.send(JSON.stringify({ 
        action: "get_user_data", 
        notificationId: notificationId 
    }));
}

// Function to update user lists in the popup
function updateUserList(users, notificationId) {
    const seenUsersList = document.getElementById('seen-users');
    const unseenUsersList = document.getElementById('unseen-users');
    
    // Clear previous lists
    seenUsersList.innerHTML = '';
    unseenUsersList.innerHTML = '';

    // Find matching notification to get subscribers list
    const notification = notificationsData.find(n => n._id === notificationId);
    const subscribedUserIds = notification ? notification.subscribed_clients : [];
    
    if (subscribedUserIds.length === 0) {
        unseenUsersList.innerHTML = '<div class="no-users">No subscribed users at send time</div>';
        return;
    }
    
    // Process each subscribed user
    users.forEach(user => {
        if (subscribedUserIds.includes(user.user_id)) {
            const userElement = document.createElement('div');
            userElement.className = 'user-item';
            
            // Check if user has the message in their messages array
            const hasMessage = user.messages.some(m => m._id === notificationId);
            const lastSeen = new Date(user.timeLogin);
            const messageTime = new Date(notification.timestamp);
            
            // Consider online users as having seen the message automatically
            const hasSeen = (hasMessage && lastSeen > messageTime) || user.online;
            
            // Determine online status
            const onlineStatus = user.online 
                ? '<span class="status-dot online" title="Online"></span>' 
                : '<span class="status-dot offline" title="Offline"></span>';
            
            // Display "Currently online" for online users instead of last login time
            const lastActiveText = user.online 
                ? 'Currently online' 
                : `Last active: ${formatDateTime(user.timeLogin)}`;
            
            userElement.innerHTML = `
                <div class="user-email">${onlineStatus} ${user.email}</div>
                <div class="user-last-seen">${lastActiveText}</div>
            `;
            
            if (hasSeen) {
                seenUsersList.appendChild(userElement);
            } else {
                unseenUsersList.appendChild(userElement);
            }
        }
    });
    
    // Handle empty lists
    if (seenUsersList.children.length === 0) {
        seenUsersList.innerHTML = '<div class="no-users">No users have seen this message yet</div>';
    }
    
    if (unseenUsersList.children.length === 0) {
        unseenUsersList.innerHTML = '<div class="no-users">All subscribed users have seen this message</div>';
    }
}

// Set up event listeners
document.querySelector('.close-btn').addEventListener('click', () => {
    document.getElementById('popup').classList.add('hidden');
    currentViewedNotification = null;
});

document.getElementById('popup').addEventListener('click', (e) => {
    if (e.target.id === 'popup') {
        document.getElementById('popup').classList.add('hidden');
        currentViewedNotification = null;
    }
});