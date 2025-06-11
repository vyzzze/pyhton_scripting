import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for i, voice in enumerate(voices):
    print(f"[{i}] {voice.name} - {voice.languages} - {voice.id}")
