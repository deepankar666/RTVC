from flask import Flask, render_template, request, jsonify
from mtranslate import translate
import gtts
import os
import time
import pygame

app = Flask(__name__)

def recognize_translate_play(text):
    translation = translate(text, "hi")  # Translate to Hindi

    # Define the path where the audio files will be saved
    audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
    os.makedirs(audio_dir, exist_ok=True)

    # Generate a unique filename based on the current timestamp
    timestamp = int(time.time())
    audio_file = os.path.join(audio_dir, f"tmp_audio_{timestamp}.mp3")

    converted_audio = gtts.gTTS(translation, lang="hi")  # Convert to speech in Hindi
    converted_audio.save(audio_file)
    print("Saved audio file:", audio_file)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # Wait for the playback to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Adjust the frequency of checking

    pygame.quit()  # Clean up Pygame

    return audio_file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        text = request.json['text']
        audio_file = recognize_translate_play(text)
        return jsonify({'audio_file': os.path.basename(audio_file)})

if __name__ == "__main__":
    app.run(debug=True)
