import speech_recognition
import pyttsx3
import pyautogui

class speechDetector():
    def __init__(self):
        pass

    def speechRecognition():

        recognizer = speech_recognition.Recognizer()

        while True:

            try:
                with speech_recognition.Microphone() as mic:

                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    text = recognizer.recognize_google(audio)
                    text = text.lower()

                    print("Text: " + text)

                    if text == "exit":
                        break

            except:
                print("(Wating for word)")
                recognizer = speech_recognition.Recognizer()
                continue

        print("Thank you for your time")
