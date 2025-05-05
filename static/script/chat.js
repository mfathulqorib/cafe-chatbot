class ChatManager {
    constructor() {
        this.chatForm = document.getElementById('chat-form');
        this.userInput = document.getElementById('user-input');
        this.chatMessages = document.getElementById('chat-messages');
        this.submitBtn = document.getElementById('submit-btn');
        this.ws = null;
        this.typingEl = 
        `<div class="flex space-x-1">
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 200ms"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 400ms"></div>
        </div>`
        
        this.init();
    }

    init() {
        this.connectWebSocket();
        this.setupEventListeners();
        this.userInput.focus();
    }

    connectWebSocket() {
        try {
            this.ws = new WebSocket("ws://localhost:8000/ws/chats/");
            
            this.ws.onopen = () => {
                console.log("Connected to WebSocket server");
            };

            this.ws.onclose = () => {
                console.log("Disconnected from WebSocket server");
                // Attempt to reconnect after 5 seconds
                setTimeout(() => this.connectWebSocket(), 5000);
            };

            this.ws.onerror = (error) => {
                console.error("WebSocket error:", error);
            };

            this.ws.onmessage = (event) => {
                try {
                    const responseMessage = JSON.parse(event.data).message;
                    const typingIndicatorEl = document.getElementById('typing-indicator');

                    typingIndicatorEl.remove();
                    this.addMessage(responseMessage, false);
                } catch (error) {
                    console.error("Error parsing message:", error);
                }
            };
        } catch (error) {
            console.error("Error connecting to WebSocket:", error);
        }
    }

    setupEventListeners() {
        this.userInput.addEventListener('input', () => {
            this.submitBtn.disabled = !this.userInput.value.trim();
        });

        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const message = this.userInput.value.trim();
            
            if (message) {
                this.sendMessage(message);
                this.userInput.value = '';
                this.submitBtn.disabled = true;
            }
        });
    }

    sendMessage(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ message }));
            this.addMessage(message);
            this.addMessage(this.typingEl, 'typing-indicator');
        } else {
            console.error("WebSocket is not connected");
            this.addMessage("Sorry, I'm having trouble connecting. Please try again later.", false);
        }
    }

    addMessage(content, role = "user") {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex ${role == 'typing-indicator' ? 'items-center' : 'items-start'} ${role == 'user' ? 'justify-end' : ''}`;
        messageDiv.id = role == 'typing-indicator' ? 'typing-indicator' : '';
        
        const userIcon = `
            <div class="w-8 h-8 rounded-full ${role == 'user' ? 'bg-gray-300' : 'bg-blue-500'} flex items-center justify-center ${role == 'user' ? 'text-gray-600' : 'text-white'}">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    ${role == 'user' ? 
                        '<path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />' :
                        '<path d="M2 10a8 8 0 1116 0 8 8 0 01-16 0zm8 1a1 1 0 100-2 1 1 0 000 2zm-.5-6a.5.5 0 00-.5.5v4a.5.5 0 001 0v-4a.5.5 0 00-.5-.5z" />'
                    }
                </svg>
            </div>
        `;

        const messageContent = `
            <div class="${role == 'user' ? 'mr-2 bg-blue-500' : 'ml-2 bg-gray-100'} rounded-lg py-2 px-4 max-w-[75%]">
                <p class="${role == 'user' ? 'text-white' : 'text-gray-800'}">${content}</p>
            </div>
        `;

        messageDiv.innerHTML = role == 'user' ? 
            `${messageContent}${userIcon}` : 
            `${userIcon}${messageContent}`;

        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    cleanup() {
        if (this.ws) {
            this.ws.close();
        }
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