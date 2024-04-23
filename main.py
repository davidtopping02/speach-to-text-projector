from vosk import Model, KaldiRecognizer
import os
import pyaudio

# Ensure you replace 'path_to_model_directory' with the actual path to your downloaded and extracted model
model_path = 'vosk-model-small-en-us-0.15/'
if not os.path.exists(model_path):
    print("Model path is incorrect. Please adjust the model_path variable.")
    exit(1)

model = Model(model_path)

# Initialize pyaudio and open a stream to capture microphone input
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4000)
stream.start_stream()

# Initialize the recognizer with the model
recognizer = KaldiRecognizer(model, 16000)

print("Please speak...")

# Process microphone audio via Vosk
while True:
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        print(result)
    else:
        # You can comment this line if you don't want partial results
        print(recognizer.PartialResult())

# Don't forget to stop and close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()
