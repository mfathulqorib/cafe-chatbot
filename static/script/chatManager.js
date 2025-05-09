// Configuration
const CONFIG = {
    WS_URL: "ws://localhost:8000/ws/chats/",
    RECONNECT_DELAY: 5000,
    MAX_RECONNECT_ATTEMPTS: 5
};

// Message templates
const TEMPLATES = {
    typingIndicator: `
        <div class="flex space-x-1">
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 200ms"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 400ms"></div>
        </div>`,
    userIcon: (role) => `
        <div class="w-8 h-8 rounded-full ${role === 'user' ? 'bg-gray-300' : 'bg-blue-500'} flex items-center justify-center ${role === 'user' ? 'text-gray-600' : 'text-white'}">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                ${role === 'user' ? 
                    '<path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />' :
                    '<path d="M2 10a8 8 0 1116 0 8 8 0 01-16 0zm8 1a1 1 0 100-2 1 1 0 000 2zm-.5-6a.5.5 0 00-.5.5v4a.5.5 0 001 0v-4a.5.5 0 00-.5-.5z" />'
                }
            </svg>
        </div>`
};

class ChatManager {
    constructor() {
        this.chatForm = document.getElementById('chat-form');
        this.userInput = document.getElementById('user-input');
        this.chatMessages = document.getElementById('chat-messages');
        this.submitBtn = document.getElementById('submit-btn');

        this.latestId = null;
        this.ws = null;
        this.reconnectAttempts = 0;
        
        this.init();
    }

    init() {
        this.connectWebSocket();
        this.setupEventListeners();
        this.userInput.focus();
    }

    connectWebSocket() {
        try {
            this.ws = new WebSocket(CONFIG.WS_URL);
            this.setupWebSocketHandlers();
        } catch (error) {
            this.handleWebSocketError(error);
        }
    }

    setupWebSocketHandlers() {
        this.ws.onopen = () => {
            console.log("Connected to WebSocket server");
            this.reconnectAttempts = 0;
        };

        this.ws.onclose = () => {
            console.log("Disconnected from WebSocket server");
            this.handleReconnection();
        };

        this.ws.onerror = (error) => {
            console.error("WebSocket error:", error);
            this.handleWebSocketError(error);
        };

        this.ws.onmessage = this.handleWebSocketMessage.bind(this);
    }

    handleWebSocketMessage(event) {
        const typingIndicatorEl = document.getElementById('typing-indicator');
        if (typingIndicatorEl) {
            typingIndicatorEl.remove();
        }
        
        try {
            const data = JSON.parse(event.data).message;
            this.processMessage(data);
        } catch (error) {
            console.error("Error parsing message:", error);
            this.showErrorMessage("Sorry, I'm having trouble processing the message. Please try again.");
        }
    }

    processMessage(data) {
        const { content, stream_status } = data;
        
        switch (stream_status) {
            case "start_stream":
                this.addMessage(content, false);
                break;
            case "on_progress":
                this.appendMessage(content);
                break;
            case "stream_end":
                this.parseMessage();
                break;
            default:
                console.warn("Unknown stream status:", stream_status);
        }
    }

    handleReconnection() {
        if (this.reconnectAttempts < CONFIG.MAX_RECONNECT_ATTEMPTS) {
            this.reconnectAttempts++;
            setTimeout(() => this.connectWebSocket(), CONFIG.RECONNECT_DELAY);
        } else {
            this.showErrorMessage("Connection lost. Please refresh the page to reconnect.");
        }
    }

    handleWebSocketError(error) {
        console.error("WebSocket error:", error);
        this.showErrorMessage("Connection error. Please check your internet connection and try again.");
    }

    showErrorMessage(message) {
        this.addMessage(message, false);
    }

    setupEventListeners() {
        this.userInput.addEventListener('input', () => {
            this.submitBtn.disabled = !this.userInput.value.trim();
        });

        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleMessageSubmission();
        });
    }

    handleMessageSubmission() {
        const message = this.userInput.value.trim();
        if (message) {
            this.sendMessage(message);
            this.userInput.value = '';
            this.submitBtn.disabled = true;
        }
    }

    sendMessage(message) {
        this.addMessage(message);

        if (this.isWebSocketReady()) {
            this.ws.send(JSON.stringify({ message }));
            this.addMessage(TEMPLATES.typingIndicator, 'typing-indicator');
        } else {
            this.showErrorMessage("Connection lost. Please refresh the page to reconnect.");
        }
    }

    isWebSocketReady() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }

    addMessage(content, role = "user") {
        this.latestId = this.generateId();

        const messageDiv = document.createElement('div');
        messageDiv.className = `flex ${role === 'typing-indicator' ? 'items-center' : 'items-start'} ${role === 'user' ? 'justify-end' : ''}`;
        messageDiv.id = role === 'typing-indicator' ? 'typing-indicator' : '';
        
        const messageContent = `
            <div class="${role === 'user' ? 'mr-2 bg-blue-500' : 'ml-2 bg-gray-50'} rounded-lg py-2 px-4 max-w-[75%]">
                <p id="${this.latestId}" class="${role === 'user' ? 'text-white' : 'text-gray-800'}">${content}</p>
            </div>
        `;
        
        messageDiv.innerHTML = role === 'user' ? 
            `${messageContent}${TEMPLATES.userIcon(role)}` : 
            `${TEMPLATES.userIcon(role)}${messageContent}`;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    appendMessage(content) {
        const messageEl = document.getElementById(this.latestId);
        if (messageEl) {
            messageEl.innerText += content;
            this.scrollToBottom();
        }
    }

    parseMessage() {
        const messageEl = document.getElementById(this.latestId);
        if (messageEl) {
            console.log(messageEl.innerHTML);
            messageEl.innerHTML = marked.parse(messageEl.innerHTML);
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    cleanup() {
        if (this.ws) {
            this.ws.close();
        }
    }

    generateId() {
        return crypto.randomUUID();
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const chatManager = new ChatManager();
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        chatManager.cleanup();
    });
});