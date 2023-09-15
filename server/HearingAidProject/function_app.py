import azure.functions as func
import logging
import azure.cognitiveservices.speech as speechsdk
import io
import os
import uuid
import base64

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.FUNCTION)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    # Generate a unique ID for the request
    request_id = str(uuid.uuid4())

    logging.info(f'Request {request_id}: Python HTTP trigger function processed a request.')

    try:
        logging.info(f'Request {request_id}: Getting audio data from request body')

        # Get the audio data from the HTTP request query string
        #audio_data = req.params.get('audio_data')
        audio_data = req.get_body()

        audio_data = base64.b64decode(audio_data)

        # Recognize the speech
        recognized_text = recognize_speech(audio_data)
        
        # Return the recognized text as an HTTP response
        return func.HttpResponse(recognized_text)
    
    except Exception as e:
        logging.error(f'Request {request_id}: Exception occurred: {str(e)}')
        return func.HttpResponse(str(e))


def recognize_speech(audio_data):
    if not audio_data:
        raise ValueError("Audio data is empty")
    
    speech_config = speechsdk.SpeechConfig(subscription='96793844213644ec9c7ec5fe0db28992', region='uksouth')
    speech_config.speech_recognition_language="en-US"

    # Create an audio input stream from the raw audio data
    audio_stream = speechsdk.audio.AudioInputStream(audio_data)

    # Create an audio config from the audio input stream
    audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)

    return "ready to recognise"

    # Create a speech recognizer with the audio config
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return ""
