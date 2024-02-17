from flask import Flask, request
from gtts import gTTS
import random
import string
import os
import subprocess
from deep_translator import GoogleTranslator

app = Flask(__name__)

def recognize_translate_play(text):
    try:
        translation = GoogleTranslator(source='auto', target='hi').translate(text)
        translated_text = translation
        print("Translated Text:", translated_text)

        # Generate a random filename for the audio file
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.mp3'
        audio_file = os.path.join(os.path.dirname(__file__), 'audio', filename)

        # Create the audio file
        tts = gTTS(text=translated_text, lang='hi')
        tts.save(audio_file)

        # Play the audio file
        subprocess.Popen(['xdg-open', audio_file])
    except Exception as e:
        print("Error:", e)
        # Handle the error gracefully, such as logging the error or displaying a message to the user

@app.route('/translate', methods=['POST'])
def translate():
    try:
        text = request.json['text']
        recognize_translate_play(text)
        return {'message': 'Translation successful'}, 200
    except KeyError:
        return {'error': 'Missing text in request'}, 400
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
