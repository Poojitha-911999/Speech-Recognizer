import speech_recognition as sr
import difflib

def recognize_speech_from_mic():
    """Capture audio from the microphone and convert it to text."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)  # reduce background noise
        print("Listening...")
        audio = recognizer.listen(source,10)
    
    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio,language='en-in')  # use Google's speech recognition
        print(f"Recognized Text: {text}")
        return text.lower()  # return recognized text in lowercase for comparison
    except sr.RequestError:
        # API was unreachable or unresponsive
        print("API unavailable")
        return None
    except sr.UnknownValueError:
        # Speech was unintelligible
        print("Unable to recognize speech")
        return None

def compare_pronunciation(expected_sentence, spoken_sentence):
    """Compare the expected sentence with the spoken one and provide feedback."""
    # Use difflib to get a similarity ratio between the sentences
    similarity = difflib.SequenceMatcher(None, expected_sentence.lower(), spoken_sentence.lower()).ratio()
    
    # Provide feedback based on the similarity ratio
    if similarity > 0.95:  # you can adjust this threshold
        return f"Pronunciation is correct! (Similarity: {similarity:.2f})"
    else:
        return f"Pronunciation is incorrect. (Similarity: {similarity:.2f})"

def evaluate_pronunciation(expected_sentence):
    """Evaluate the correctness of the user's pronunciation."""
    print(f"Expected Sentence: {expected_sentence}")
    
    # Get spoken sentence from the user
    spoken_sentence = recognize_speech_from_mic()
    print(spoken_sentence)
    if spoken_sentence is not None:
        # Compare and provide feedback
        feedback = compare_pronunciation(expected_sentence, spoken_sentence)
        print(feedback)
    else:
        print("Could not evaluate pronunciation due to recognition failure.")

# Example usage
if __name__ == "__main__":
    expected_sentence = "Poojitha is hiered successfully"
    evaluate_pronunciation(expected_sentence)
