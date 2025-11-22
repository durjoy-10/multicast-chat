class MulticastChat {
    constructor() {
        this.socket = null;
        this.username = '';
        this.isConnected = false;
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Enter key support
        document.getElementById('usernameInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.joinChat();
        });

        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    connect() {
        this.socket = io('http://localhost:5000');
        
        this.socket.on('connect', () => {
            this.updateStatus('connected', 'Connected');
            this.isConnected = true;
        });

        this.socket.on('disconnect', () => {
            this.updateStatus('disconnected', 'Disconnected');
            this.isConnected = false;
        });

        this.socket.on('receive_message', (data) => {
            this.displayMessage(data);
        });

        this.socket.on('user_joined', (data) => {
            this.displaySystemMessage(data.message);
            this.updateUserCount(data.user_count);
            this.getUsers();
        });

        this.socket.on('user_left', (data) => {
            this.displaySystemMessage(data.message);
            this.updateUserCount(data.user_count);
            this.getUsers();
        });

        this.socket.on('users_list', (data) => {
            this.updateUsersList(data.users);
        });
    }

    joinChat() {
        const usernameInput = document.getElementById('usernameInput');
        const username = usernameInput.value.trim();

        if (!username) {
            alert('Please enter a username');
            return;
        }

        this.username = username;
        
        if (!this.socket) {
            this.connect();
        }

        this.socket.emit('join', { username: username });
        
        // Show chat interface
        document.getElementById('loginSection').style.display = 'none';
        document.getElementById('chatContainer').style.display = 'flex';
        
        // Focus message input
        document.getElementById('messageInput').focus();
    }

    sendMessage() {
        if (!this.isConnected) return;

        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();

        if (!message) return;

        this.socket.emit('send_message', { message: message });
        messageInput.value = '';
    }

    displayMessage(data) {
        const messagesContainer = document.getElementById('messages');
        const messageElement = document.createElement('div');
        
        const isOwnMessage = data.user_id === this.socket.id;
        const messageClass = isOwnMessage ? 'message own' : 'message other';
        
        const timestamp = new Date(data.timestamp).toLocaleTimeString();
        
        messageElement.className = messageClass;
        messageElement.innerHTML = `
            <div class="message-header">
                <strong>${data.username}</strong>
                <span>${timestamp}</span>
            </div>
            <div class="message-content">${this.escapeHtml(data.message)}</div>
        `;
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    displaySystemMessage(message) {
        const messagesContainer = document.getElementById('messages');
        const messageElement = document.createElement('div');
        
        messageElement.className = 'message system';
        messageElement.textContent = message;
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    updateUsersList(users) {
        const usersList = document.getElementById('usersList');
        usersList.innerHTML = '';
        
        users.forEach(username => {
            const userElement = document.createElement('div');
            userElement.className = 'user-item';
            userElement.textContent = username;
            usersList.appendChild(userElement);
        });
    }

    updateUserCount(count) {
        document.getElementById('userCount').textContent = `${count} users online`;
    }

    updateStatus(status, text) {
        const statusElement = document.getElementById('status');
        statusElement.textContent = text;
        statusElement.className = status;
    }

    getUsers() {
        if (this.socket) {
            this.socket.emit('get_users');
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chat = new MulticastChat();
});

// Global functions for HTML onclick handlers
function joinChat() {
    window.chat.joinChat();
}

function sendMessage() {
    window.chat.sendMessage();
}