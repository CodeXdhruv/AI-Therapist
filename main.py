import pyaudio
import wave
import whisper
from gtts import gTTS
from playsound import playsound
import google.generativeai as genai
import numpy as np
import queue
import threading

# Set your Gemini API key here
genai.configure(api_key="AIzaSyCZplIDyFE70eJLrCbEVl0Zi1y-k8VYLWI")

# === Recording Settings ===
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000  # Whisper expects 16kHz
CHUNK = 1024
RECORD_SECONDS = 5

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file

def record_audio_realtime():
    print("🎙️ Recording... Speak now.")
    audio = pyaudio.PyAudio()
    audio_queue = queue.Queue()

    def audio_callback(in_data, frame_count, time_info, status):
        audio_queue.put(np.frombuffer(in_data, dtype=np.float32))
        return (in_data, pyaudio.paContinue)

    stream = audio.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK,
                       stream_callback=audio_callback)

    stream.start_stream()
    
    # Collect audio for RECORD_SECONDS
    audio_data = []
    for _ in range(int(RATE * RECORD_SECONDS / CHUNK)):
        audio_data.append(audio_queue.get())
    
    print("✅ Recording complete.")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return np.concatenate(audio_data)

def transcribe_audio_realtime(audio_data):
    print("📝 Transcribing...")
    model = whisper.load_model("base")
    
    # Convert audio data to float32 for Whisper
    audio_data = audio_data.astype(np.float32)
    # Normalize the audio data
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    result = model.transcribe(audio_data)
    print("User said:", result["text"])
    return result["text"]

# Add at the top with other imports
conversation_history = []

def generate_therapy_response(user_text):
    # Include conversation history in the prompt
    history_text = "\n".join([f"User: {h['user']}\nTherapist: {h['therapist']}" for h in conversation_history])
    prompt = f"""You are a concise and precise cognitive behavioral therapist. 
    Provide brief, focused responses that address the core concern.
    Keep responses under 3 sentences.
    
    Previous conversation:
    {history_text}
    
    User's message: "{user_text}" """

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    
    # Store the conversation
    conversation_history.append({"user": user_text, "therapist": response.text})
    print("🧠 Therapist response:", response.text)
    return response.text

def run_ai_therapist():
    print("👂 Welcome to the Voice AI Therapist")
    print("Say or type 'goodbye' to end the session")
    
    while True:
        print("\nHow would you like to communicate?")
        print("1. Voice Input")
        print("2. Text Input")
        
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "1":
            audio_data = record_audio_realtime()
            user_text = transcribe_audio_realtime(audio_data)
        elif choice == "2":
            user_text = get_text_input()
        else:
            print("Invalid choice. Defaulting to text input.")
            user_text = get_text_input()
        
        # Check for goodbye
        if user_text.lower().strip() == "goodbye":
            print("Thank you for the session. Take care! 👋")
            break
        
        ai_response = generate_therapy_response(user_text)
        speak_text(ai_response)

import pyttsx3  # Add this import at the top

def speak_text(text, output_file="response.mp3"):
    print("🔊 Converting to speech...")
    engine = pyttsx3.init()
    
    # Configure voice settings
    engine.setProperty('rate', 150)  # Speed up the speech (normal is 150)
    engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Use female voice
    
    # Speak the text
    engine.say(text)
    engine.runAndWait()

def get_text_input():
    print("💬 Please type your message:")
    return input("> ")

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_text = request.json.get('message')
    response = generate_therapy_response(user_text)
    return jsonify({'response': response})

@app.route('/api/voice', methods=['POST'])
def voice():
    audio_data = request.files['audio'].read()
    text = transcribe_audio_realtime(audio_data)
    response = generate_therapy_response(text)
    return jsonify({
        'text': text,
        'response': response
    })

@app.route('/api/speak', methods=['POST'])
def speak():
    try:
        text = request.json.get('text')
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('voice', engine.getProperty('voices')[1].id)
        
        # Save audio to a temporary file
        temp_file = "temp_speech.wav"
        engine.save_to_file(text, temp_file)
        engine.runAndWait()
        
        # Send the audio file
        return send_file(temp_file, mimetype='audio/wav')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        return '', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
    run_ai_therapist()
