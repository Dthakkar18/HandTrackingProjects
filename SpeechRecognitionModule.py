import speech_recognition
import pyttsx3
import pyautogui as pag

class speechDetector():
    def __init__(self):
        pass

    def speechRecognition(self):

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

                    pag.write(text, interval=0.25)

            except:
                print("(Wating for word)")
                recognizer = speech_recognition.Recognizer()
                continue

        print("Thank you for your time")

def main():
    speech = speechDetector().speechRecognition()
    print(speech)


if __name__ == "__main__":
    main()
