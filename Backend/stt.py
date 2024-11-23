import whisper
import sounddevice as sd
import numpy as np
import threading
import webrtcvad
from IPython.display import display, clear_output

# Load the Whisper model
model = whisper.load_model("base")

# Audio parameters
RATE = 16000
CHUNK = int(RATE / 100)

# Initialize VAD
vad = webrtcvad.Vad(2)

# Buffer to hold audio data
audio_buffer = []
silence_threshold = 30
silence_counter = 0
stop_flag = False
transcriptions = []

def is_speech(audio_data):
    """Detect if the given audio chunk contains speech."""
    audio_bytes = audio_data.astype(np.int16).tobytes()
    return vad.is_speech(audio_bytes, RATE)

def callback(indata, frames, time, status):
    """Callback function for audio input."""
    global silence_counter, stop_flag
    if stop_flag:
        raise sd.CallbackStop()
    audio_data = indata[:, 0] * 32768  # scale to int16 range
    if is_speech(audio_data):
        silence_counter = 0
        audio_buffer.append(audio_data)
    else:
        silence_counter += 1
    if silence_counter > silence_threshold and len(audio_buffer) > 0:
        clear_output(wait=True)
        print("Transcribing...")
        audio_input = np.concatenate(audio_buffer).astype(np.float32) / 32768.0
        result = model.transcribe(audio_input, language='en', fp16=False)
        transcript_text = result["text"]
        transcriptions.append(transcript_text)
        display("Transcription: " + transcript_text)
        audio_buffer.clear()
        silence_counter = 0

def listen_for_enter_key():
    """Wait for the user to press Enter to stop transcription."""
    global stop_flag
    input("Press Enter to stop transcription...\n")
    stop_flag = True

def start_transcription():
    """Start the transcription process and return the final transcription text."""
    global stop_flag, transcriptions
    stop_flag = False
    transcriptions.clear()

    # Start the audio stream
    stream = sd.InputStream(callback=callback, channels=1, samplerate=RATE, blocksize=CHUNK)
    stream.start()

    # Start a separate thread to listen for Enter key
    transcription_thread = threading.Thread(target=listen_for_enter_key)
    transcription_thread.start()

    # Wait for the transcription thread to finish
    transcription_thread.join()

    # Stop and close the audio stream
    stream.stop()
    stream.close()

    # Combine all transcriptions into a complete transcript
    complete_transcript = " ".join(transcriptions)
    print("\nComplete Transcript:\n", complete_transcript)
    
    return complete_transcript