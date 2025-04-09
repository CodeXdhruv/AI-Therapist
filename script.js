let users = JSON.parse(localStorage.getItem('users')) || {};

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (users[username] === password) {
        document.getElementById('loginPage').style.display = 'none';
        document.getElementById('chatPage').style.display = 'block';
        updateChat("Welcome to AI Therapist! Type or speak your message, or type 'goodbye' to end the session.", "System");
    } else {
        alert("Invalid username or password");
    }
}

function showRegister() {
    document.getElementById('loginPage').style.display = 'none';
    document.getElementById('registerPage').style.display = 'block';
}

function register() {
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;

    if (username === "" || password === "") {
        alert("Please enter valid username and password");
        return;
    }

    if (users[username]) {
        alert("Username already exists");
        return;
    }

    users[username] = password;
    localStorage.setItem('users', JSON.stringify(users));
    alert("Account created successfully!");
    
    document.getElementById('registerPage').style.display = 'none';
    document.getElementById('loginPage').style.display = 'block';
}

function updateChat(message, sender) {
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const chatDisplay = document.getElementById('chatDisplay');
    chatDisplay.innerHTML += `[${timestamp}] ${sender}: ${message}<br>`;
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

document.getElementById('messageInput').addEventListener('keypress', async function(e) {
    if (e.key === 'Enter') {
        const message = this.value.trim();
        if (!message) return;

        if (message.toLowerCase() === 'goodbye') {
            updateChat("Thank you for the session. Take care! 👋", "System");
            setTimeout(() => window.location.reload(), 2000);
            return;
        }

        this.value = '';
        updateChat(message, "You");
        
        // Call the API
        document.getElementById('status').textContent = "Thinking...";
        try {
            const response = await fetch('http://localhost:5000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            updateChat(data.response, "Therapist");
            
            // Add voice output
            document.getElementById('status').textContent = "Speaking...";
            await speakResponse(data.response);
            document.getElementById('status').textContent = "";
        } catch (error) {
            updateChat("Sorry, I'm having trouble connecting to the server.", "System");
            console.error(error);
        }
        document.getElementById('status').textContent = "";
    }
});

// Add new function for text-to-speech
async function speakResponse(text) {
    try {
        const response = await fetch('http://localhost:5000/api/speak', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        await audio.play();
        URL.revokeObjectURL(audioUrl);  // Clean up
    } catch (error) {
        console.error('Speech synthesis error:', error);
    }
}

// Update voice input handler to include speech output
async function startVoiceInput() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        const audioChunks = [];

        document.getElementById('status').textContent = "Recording...";
        
        mediaRecorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", async () => {
            const audioBlob = new Blob(audioChunks);
            const formData = new FormData();
            formData.append('audio', audioBlob);

            try {
                const response = await fetch('http://localhost:5000/api/voice', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                updateChat(data.text, "You");
                updateChat(data.response, "Therapist");
                
                // Add voice output for voice inputs
                document.getElementById('status').textContent = "Speaking...";
                await speakResponse(data.response);
                document.getElementById('status').textContent = "";
            } catch (error) {
                updateChat("Sorry, I'm having trouble processing your voice input.", "System");
                console.error(error);
            }
            document.getElementById('status').textContent = "";
        });

        mediaRecorder.start();
        setTimeout(() => {
            mediaRecorder.stop();
            stream.getTracks().forEach(track => track.stop());
        }, 5000); // Record for 5 seconds
    } catch (error) {
        alert("Please allow microphone access to use voice input");
        console.error(error);
    }
}