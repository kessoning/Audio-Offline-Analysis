import argparse
import librosa
import os
import subprocess
import tkinter as tk
from tkinter import filedialog

def convert_to_wav(input_file):
    output_file = "temp.wav"
    subprocess.call(["ffmpeg", "-i", input_file, output_file])
    return output_file

def save_beat_frames(input_file, fps, output_file, mul):
    convert_temp_wav = False

    # Convert input file to WAV if it is not already in WAV format
    if not input_file.lower().endswith('.wav'):
        input_file = convert_to_wav(input_file)
        convert_temp_wav = True

    # Load the audio file
    y, sr = librosa.load(input_file)

    # Use the onset detection function
    onset_env = librosa.onset.onset_strength(y, sr=sr)

    # Detect the beats
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # Convert beat frames to frame numbers
    frame_numbers = librosa.frames_to_samples(beat_frames)

    # Calculate the frame numbers corresponding to the beats
    beat_frames_animation = (frame_numbers * fps / sr).astype(int)

    # Generate the frame-by-frame output with multiplier
    output = []
    for i in range(len(y)):
        if i in beat_frames_animation:
            output.append(f"{i}:({1 * mul}),")
        else:
            output.append(f"{i}:(0),")

    # Add .txt extension to the output file if it is not present
    if not output_file.lower().endswith('.txt'):
        output_file = output_file + ".txt"

    # Save the frame-by-frame output to a text file
    with open(output_file, 'w') as f:
        f.write('\n'.join(output))

    print("Frame-by-frame output saved to:", output_file)

    # Delete temporary WAV file if it was converted
    if convert_temp_wav:
        os.remove(input_file)
        print("Temporary WAV file deleted.")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.ogg *.mp4")])
    entry_input.delete(0, tk.END)
    entry_input.insert(tk.END, file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt")])
    entry_output.delete(0, tk.END)
    entry_output.insert(tk.END, file_path)

def process():
    input_file = entry_input.get()
    fps = int(entry_fps.get())
    output_file = entry_output.get()
    mul = float(entry_mul.get())

    save_beat_frames(input_file, fps, output_file, mul)

# Create the main window
window = tk.Tk()
window.title("Beat Detection Script")

# Input file selection
label_input = tk.Label(window, text="Input Audio File:")
label_input.pack()
entry_input = tk.Entry(window)
entry_input.pack()
button_input = tk.Button(window, text="Browse", command=open_file)
button_input.pack()

# FPS input
label_fps = tk.Label(window, text="Frames per Second (FPS):")
label_fps.pack()
entry_fps = tk.Entry(window)
entry_fps.pack()

# Output file selection
label_output = tk.Label(window, text="Output File:")
label_output.pack()
entry_output = tk.Entry(window)
entry_output.pack()
button_output = tk.Button(window, text="Browse", command=save_file)
button_output.pack()

# Multiplier input
label_mul = tk.Label(window, text="Multiplier:")
label_mul.pack()
entry_mul = tk.Entry(window)
entry_mul.pack()

# Process button
button_process = tk.Button(window, text="Process", command=process)
button_process.pack()

# Run the GUI main loop
window.mainloop()
