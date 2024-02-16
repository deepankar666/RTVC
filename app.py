from flask import Flask, request, jsonify
from gtts import gTTS
import os
import random
import string
import subprocess
import time
import googletrans
from googletrans import Translator

app = Flask(__name__)

translator = Translator()

def recognize_translate_play(text):
    translation = translator.translate(text, dest="hi")  # Translate to Hindi
    translated_text = translation.text
    print("Translated Text:", translated_text)
    
    # Generate a random filename for the audio file
    filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.mp3'
    audio_file = os.path.join(os.path.dirname(__file__), 'audio', filename)

    # Create the audio file
    tts = gTTS(text=translated_text, lang='hi')
    tts.save(audio_file)

    # Play the audio file
    subprocess.Popen(['xdg-open', audio_file])

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        text = request.json['text']
        recognize_translate_play(text)
        return jsonify({'message': 'Translation success'}), 200
    else:
        return jsonify({'error': 'Invalid request method'}), 405

if __name__ == '__main__':
    app.run(debug=True)
