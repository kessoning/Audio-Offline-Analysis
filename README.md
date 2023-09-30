# Offline Audio Analyzer and Beat Detection

[![License](https://img.shields.io/github/license/your-username/your-repo.svg)](LICENSE)

An offline audio analyzer and beat detection tool for creating sound-reactive animations and keyframes. This project utilizes the power of the librosa library to analyze audio tracks and extract beat information, enabling the creation of synchronized animations offline.

Please note that this tool is designed for offline use and does not provide real-time audio analysis. It is intended for situations where you need to generate sound-reactive animations in high resolutions or perform complex visual processing on top of them.

## Reasons

I typically develop visuals in creative coding environments like Processing, OpenFrameworks, and OpenGL. When it comes to delivering a final, high-resolution video, I often struggle to find an efficient way to render my visuals at the desired quality. Screen recording doesn't quite cut it, especially with complex visuals, and real-time rendering becomes challenging.

That's why I've developed a script that saves volume data for each frame and allows for precise frame-by-frame recall. I believe this tool can benefit other creative coders facing similar challenges. Let's simplify our workflow and support each other in our creative endeavors!

## Features

- Analyze audio tracks offline for sound-reactive animations.
- Detect beats and extract frame numbers for synchronization.
- Create keyframes for use with Stable Diffusion Deforum to generate sound-reactive animations.
- Customizable output formula for each frame based on audio values.

## Usage

Be sure to have the latest version of [FFMPEG](https://ffmpeg.org/) installed on your machine.

### Windows executable

Grab this user-friendly Windows executable right over [here!](https://github.com/kessoning/Audio-Offline-Analysis/releases/tag/v0.1)

### Python script

Or run the script on any OS (well, at least I hope so!) by yourself:

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Run the script using the provided command-line arguments.
   ```bash
   python audio_to_params.py --input input.wav --fps 30 --output data.txt --formula "1 + x * 2"
   python beat_detection.py --input input.wav --fps 30 --output beatmap.txt 
3. Replace input.wav with the path to your audio file, 30 with the desired frames per second (FPS) of the animation, data.txt/beatmap.txt with the output file path to save the beat frames, and "1 + x * 2" with your desired formula (in the audio_to_params).
4. Utilize the generated beat frames or keyframes in your creative coding IDE (e.g., Processing, OpenFrameworks) or Stable Diffusion Deforum script.

### Understanding the Formula Usage in the Script

The audio_to_params.py script processes an audio file to generate an output that is based on a user-defined formula. The formula is applied to each sample of audio data, allowing for customizable audio analysis. The key functionality of formula evaluation is encapsulated within the evaluate_formula and main functions, with the latter being where the formula is applied to the audio data.

The formula is specified through a command-line argument (-f or --formula). The default formula is x, where x represents the normalized value of the audio sample. Users can provide a custom formula, using x as the variable representing the normalized audio sample value.

The formula allows for a wide range of audio analysis possibilities. By adjusting the formula, users can manipulate the output to reflect different aspects of the audio data, making this script highly flexible and customizable for various audio analysis tasks. This is especially useful when utilizing this script in conjunction with Stable Diffusion by Deforum.

###

To compile an executable for other OS, there is the code in the GUI_code folder. You can try to compile it on your machine, and if you want to contribute make a pull request to add it to the release page.

The compilation requires pyinstaller

```bash
pip install pyinstaller
```

After doing so, you only need to run
```bash
pyinstaller --onefile script.py
```

An issue I encountered was that librosa was missing a file, due the use of Anaconda. To solve this, you need to add librosa example data to the compiler

```bash
pyinstaller --onefile --add-data "path/to/anaconda/envs/*env_name*/lib/site-packages/librosa/util/example_data;librosa/util/example_data" script.py
```

Change "path/to/anaconda/envs/*env_name*/lib/site-packages/librosa/util/example_data" to your librosa library path.

### Example

Included in this repository is a working example implemented in Processing.

The scope of this repository currently encompasses only the Processing framework. Implementation guidance for other frameworks is not provided at this moment. However, I am open to expanding the repository to include examples in additional frameworks should I have the opportunity to work on them in the future.



## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

MIT License

Copyright (c) 2023 kesson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.