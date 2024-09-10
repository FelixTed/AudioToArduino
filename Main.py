import sounddevice as sd
import tkinter as tk
import serial
import numpy as np
import threading

# Configure the serial port
ser = serial.Serial('COM3', 9600)

# Audio settings
sample_rate = 44100  # Hertz
channels = 1  # Mono audio

def send_audio_to_serial(indata, frames, time, status):
    # Flatten and convert the audio data to int16 format
    audio_data = (indata.flatten() * 32767).astype(np.int16)
    
    # Send audio data over serial in chunks
    try:
        if ser.is_open:
            for sample in audio_data:
                ser.write(sample.tobytes())
    except serial.SerialException as e:
        print(f"Serial write error: {e}")

# Flag to control the recording loop
recording = [False]
audio_thread = None

# Function to start and stop audio recording
def startAudio():
    global audio_thread

    if recording[0]:
        recording[0] = False  # Stop the recording
        controlButton.config(text='Start Audio')  # Update button text
        audio_thread.join()  # Ensure the audio thread is finished before moving on
        if ser.is_open:
            ser.close()  # Close the serial port safely after the thread is done
    else:
        if not ser.is_open:
            ser.open()  # Reopen the serial port if needed
        recording[0] = True
        controlButton.config(text='Stop Audio')  # Update button text
        # Start recording in a separate thread
        audio_thread = threading.Thread(target=record_audio)
        audio_thread.start()

def record_audio():
    with sd.InputStream(callback=send_audio_to_serial, channels=channels, samplerate=sample_rate):
        while recording[0]:
            sd.sleep(100)  # Sleep for a short period to avoid high CPU usage
    print("Audio data sent via serial!")

# Opening window
window = tk.Tk()
window.title("Send audio to visualizer")
window.geometry('300x300')

controlButton = tk.Button(window, text='Start Audio', command=startAudio)
controlButton.pack(pady=20)

# Start the Tkinter event loop
window.mainloop()
