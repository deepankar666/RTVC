from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import os
import time
import gtts
import pygame

app = Flask(__name__)

def recognize_translate_play(text):
    translation = GoogleTranslator(source='auto', target='hi').translate(text)  # Translate to Hindi

    # Define the path where the audio files will be saved
    audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
    os.makedirs(audio_dir, exist_ok=True)

    # Generate a unique filename based on current timestamp
    timestamp = int(time.time())
    audio_file = os.path.join(audio_dir, f"tmp_audio_{timestamp}.mp3")

    converted_audio = gtts.gTTS(translation, lang="hi")  # Convert to speech in Hindi
    converted_audio.save(audio_file)
    print("Saved audio file:", audio_file)

    # Check if pygame can be initialized (audio playback is possible)
    if pygame.get_init():
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Wait for the playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Adjust the frequency of checking

    # Add a delay after playback ends to ensure the file is not deleted prematurely
    time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        text = request.json['text']
        recognize_translate_play(text)
        return jsonify({'success': True})

if __name__ == "__main__":
    # Check if pygame can be initialized (audio playback is possible)
    if pygame.get_init():
        app.run(debug=True)
    else:
        print("Audio playback not available. Running in headless mode.")
