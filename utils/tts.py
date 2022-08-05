import gtts
import os
from io import BytesIO

class NewsSpeech():
    def __init__(self, text):
        self.text = text

    def speak(self):
        tts = gtts.gTTS(text=self.text, lang='en', tld ='co.in')
        return tts
        # tts.save('tts.mp3')
        # os.remove('tts.mp3')