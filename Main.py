import sounddevice as sd
import tkinter as tk
import serial
import numpy as np
import threading
import keyboard  # For detecting key presses

# Configure the serial port
ser = serial.Serial('COM3', 9600)

# Audio settings
sample_rate = 44100  # Hertz
channels = 1  # Mono audio

def send_audio_to_serial(indata, frames, time, status):
    # Flatten and convert the audio data to int16 format
    audio_data = (indata.flatten() * 32767).astype(np.int16)
    
    # Send audio data over serial in chunks
    for sample in audio_data:
        ser.write(sample.tobytes())

# Flag to control the recording loop
recording = [False]

# Function to start and stop audio recording
def startAudio():
    if recording[0]:
        recording[0] = False
        controlButton.config(text='Start Audio')  # Update button text
    else:
        recording[0] = True
        controlButton.config(text='Stop Audio')  # Update button text
        # Start recording in a separate thread
        threading.Thread(target=record_audio).start()

def record_audio():
    with sd.InputStream(callback=send_audio_to_serial, channels=channels, samplerate=sample_rate):
        while recording[0]:
            sd.sleep(100)  # Sleep for a short period to avoid high CPU usage
    # Close the serial port when recording stops
    ser.close()
    print("Audio data sent via serial!")

# Function to stop recording using keyboard input
def stop_recording(keyboard_event):
    recording[0] = False

# Register a key listener for 'q' to stop recording

# Opening window
window = tk.Tk()
window.title("Send audio to visualizer")
window.geometry('300x300')

controlButton = tk.Button(window, text='Start Audio', command=startAudio)
controlButton.pack(pady=20)

# Start the Tkinter event loop
window.mainloop()
