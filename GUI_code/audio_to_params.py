import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import argparse
import os
import numpy as np
from scipy.io import wavfile
import moviepy.editor
from tqdm import trange
import subprocess

def convert_to_wav(input_file):
    output_file = "temp.wav"
    subprocess.call(["ffmpeg", "-i", input_file, output_file])
    return output_file

def select_file():
    filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.ogg *.mp4 *.mov" )])
    if filename:
        entry_path.delete(0, tk.END)
        entry_path.insert(tk.END, filename)

def run_script():
    audio_file = entry_path.get()
    fps = int(entry_fps.get())
    output_file = entry_output.get()
    formula = entry_formula.get()

    if audio_file and fps and output_file and formula:
        try:
            convert_temp_wav = False

            # Convert input file to WAV if it is not already in WAV format
            if not audio_file.lower().endswith('.wav'):
                audio_file = convert_to_wav(audio_file)
                convert_temp_wav = True

            # Check if the input audio file exists
            if not os.path.exists(audio_file):
                # If not, convert the audio using moviepy
                audio_clip = moviepy.editor.AudioFileClip(audio_file)
                audio_clip.write_audiofile(audio_file, fps=44100, nbytes=2, codec='pcm_s16le')

            # Get the track name from the input file
            track_name = os.path.basename(audio_file)[:-4]

            # Read the audio file and convert to mono
            rate, signal = wavfile.read(audio_file)
            signal = np.mean(signal, axis=1)

            # Calculate the absolute values of the audio signal
            signal = np.abs(signal)

            # Calculate the duration, frames, and samples per frame
            duration = signal.shape[0] / rate
            frames = int(np.ceil(duration * fps))
            samples_per_frame = signal.shape[0] / frames

            # Initialize the audio array
            audio = np.zeros(frames, dtype=signal.dtype)

            # Process each frame and calculate the mean value
            for frame in range(frames):
                start = int(round(frame * samples_per_frame))
                stop = int(round((frame + 1) * samples_per_frame))
                audio[frame] = np.mean(signal[start:stop], axis=0)

            # Normalize the audio data
            audio /= np.max(audio)

            # Create an empty output string
            output = ""

            # Apply the formula to each audio sample and create the output string
            for n in trange(len(audio), desc="Sampling"):
                result = evaluate_formula(audio[n], formula)
                output += f"{n}:({result}),"

            # Add .txt extension to the output file if it is not present
            if not output_file.lower().endswith('.txt'):
                output_file = output_file + ".txt"

            # Write the output string to a text file
            with open(output_file, "w") as text_file:
                text_file.write(output)

            # Delete temporary WAV file if it was converted
            if convert_temp_wav:
                os.remove(audio_file)
                print("Temporary WAV file deleted.")

            messagebox.showinfo("Success", "Audio analysis completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during audio analysis: {str(e)}")
    else:
        messagebox.showwarning("Missing Input", "Please fill in all the required fields.")

def evaluate_formula(x, formula):
    try:
        # Safely evaluate the formula expression
        result = eval(formula, {}, {'x': x})
        return result
    except Exception as e:
        raise ValueError("Invalid formula: " + str(e))

# Create the main window
window = tk.Tk()
window.title("Audio Analysis")
window.geometry("400x250")

# Create GUI elements
label_path = tk.Label(window, text="Audio File:")
entry_path = tk.Entry(window)
button_browse = tk.Button(window, text="Browse", command=select_file)

label_fps = tk.Label(window, text="FPS:")
entry_fps = tk.Entry(window)

label_output = tk.Label(window, text="Output File:")
entry_output = tk.Entry(window)

label_formula = tk.Label(window, text="Formula:")
entry_formula = tk.Entry(window)

button_run = tk.Button(window, text="Run", command=run_script)

# Arrange the GUI elements using grid layout
label_path.grid(row=0, column=0, sticky=tk.W)
entry_path.grid(row=0, column=1, padx=10, pady=5)
button_browse.grid(row=0, column=2)

label_fps.grid(row=1, column=0, sticky=tk.W)
entry_fps.grid(row=1, column=1, padx=10, pady=5)

label_output.grid(row=2, column=0, sticky=tk.W)
entry_output.grid(row=2, column=1, padx=10, pady=5)

label_formula.grid(row=3, column=0, sticky=tk.W)
entry_formula.grid(row=3, column=1, padx=10, pady=5)

button_run.grid(row=4, column=0, columnspan=3, pady=10)

# Start the GUI event loop
window.mainloop()