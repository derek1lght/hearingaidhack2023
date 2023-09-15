import os
import sys
import azure.cognitiveservices.speech as speechsdk

def recognize_from_microphone():
    # Read from the default microphone and returns a text string

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    # setx SPEECH_KEY 96793844213644ec9c7ec5fe0db28992
    # setx SPEECH_REGION uksouth

    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))

    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))

        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


if __name__ == "__main__":
    # Get the file name from the command line arguments
    if len(sys.argv) < 2:
        print("Usage: python speech_to_text_file.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]

    # Recognize the speech from the file
    recognized_text = recognize_from_microphone()

    # Print the recognized text
    print("This is where the audio data would be sent to the Azure Function.")    

    # Write the text to a file
    with open(file_name, "w") as text_file:
        text_file.write(recognized_text)
