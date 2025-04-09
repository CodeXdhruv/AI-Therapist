# AI-Therapist
A compassionate AI chatbot offering mental health support through thoughtful conversations and voice interactions.
🧠 AI Therapist Chatbot
AI Therapist is a cognitive behavioral therapy chatbot that interacts with users via text or voice to provide supportive, brief, and targeted mental health assistance. The chatbot offers a clean, modern web interface for interaction and leverages powerful AI technologies like Google's Gemini Pro and OpenAI Whisper for speech recognition and response generation.

🌟 Features
🔐 User Authentication: Simple login and registration system using localStorage.

💬 Text-based Chat: Chat with the AI therapist by typing messages.

🎤 Voice Input Support: Speak your messages using microphone input.

🧏 Speech Recognition: Converts your voice into text using the Whisper model.

🔊 Text-to-Speech: AI responses are read aloud using pyttsx3 for enhanced engagement.

🧠 Smart AI Responses: Uses Gemini Pro (gemini-2.0-flash) for context-aware, concise CBT replies.

💡 Responsive UI: Clean dark-themed interface with styled components.

📦 ai-therapist-chatbot/
├── index.html        # Main frontend layout
├── style.css         # Styling for chatbot interface
├── script.js         # Frontend logic and API communication
├── main.py           # Backend Flask server, AI logic, and voice processing

1. Clone the repository

git clone https://github.com/yourusername/ai-therapist-chatbot.git

cd ai-therapist-chatbot

3. Install dependencies
pip install flask flask-cors pyttsx3 openai-whisper google-generativeai pyaudio numpy gtts playsound
⚠️ You may also need system dependencies for pyaudio. Use:

  sudo apt-get install portaudio19-dev (Linux)
  brew install portaudio (macOS)

5. Add your Gemini API key
Edit main.py and update:
genai.configure(api_key="YOUR_API_KEY")

6. Run the server
  python main.py
7. Open index.html in your browser
  Use Live Server in VSCode or host it with any static server tool.

🧪 Demo Walkthrough
Register or log in on the webpage.

Type your message or click the 🎤 icon to talk.

Receive AI-powered, empathetic, and concise replies.

Hear your therapist's response through speech synthesis.

🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

Voice & NLP: OpenAI Whisper, Google Gemini Pro, pyttsx3

Speech Tools: gTTS, playsound, pyaudio

AI Model: Gemini 2.0 Flash for CBT-style dialogue

💡 Future Improvements
Persistent chat history using a database

User profile and mood tracking

Therapist tone customization

Multilingual support

📄 License
This project is under the GNU License.

🤝 Acknowledgements
OpenAI Whisper
Google Gemini
Flask

