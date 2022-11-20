import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 175)

def say(content):
    engine.say(content)
    engine.runAndWait()

