import tkinter as tk
import speech_recognition as sr
import difflib

# Function to recognize speech from the microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        feedback_label.config(text="Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        feedback_label.config(text="Listening...")
        audio = recognizer.listen(source,10)
    
    try:
        feedback_label.config(text="Recognizing speech...")
        spoken_text = recognizer.recognize_google(audio,language='en-in')
        return spoken_text.lower()
    except sr.RequestError:
        feedback_label.config(text="API unavailable")
        return None
    except sr.UnknownValueError:
        feedback_label.config(text="Unable to recognize speech")
        return None

# Function to compare the expected text with the recognized speech
def evaluate_pronunciation():
    expected_sentence = entry.get().lower()
    spoken_sentence = recognize_speech()

    if spoken_sentence is not None:
        similarity = difflib.SequenceMatcher(None, expected_sentence, spoken_sentence).ratio()
        if similarity > 0.85:
            feedback_label.config(text=f"Correct pronunciation! Similarity: {similarity:.2f}")
        else:
            feedback_label.config(text=f"Incorrect pronunciation. Similarity: {similarity:.2f}\nRecognized Sentence: {spoken_sentence}")
    else:
        feedback_label.config(text="Error in recognizing speech.")

# Setting up the GUI
def setup_gui():
    root = tk.Tk()
    root.title("Pronunciation Evaluator")

    # Creating and positioning widgets
    label = tk.Label(root, text="Enter text to pronounce:")
    label.pack(pady=10)

    global entry
    entry = tk.Entry(root, width=50)
    entry.pack(pady=10)

    speak_button = tk.Button(root, text="Speak", command=evaluate_pronunciation)
    speak_button.pack(pady=10)

    global feedback_label
    feedback_label = tk.Label(root, text="", font=("Helvetica", 12))
    feedback_label.pack(pady=20)

    root.geometry("400x300")
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
