import requests
import speech_recognition as sr
import base64


# Set the URL of the HTTP GET request
url = "http://localhost:7071/api/MyHttpTrigger"

# Create a speech recognizer
r = sr.Recognizer()

def main():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    # Send the audio data as an HTTP POST request
    #response = requests.post(url, data=audio.get_wav_data())

    audio_data = base64.b64encode(audio.get_wav_data())

    response = requests.post(url, data=audio_data,
                             headers={"application/octet-stream"})

    # Print the recognized text
    print(response.text)

if __name__ == "__main__":
    main()