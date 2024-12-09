# Audio Recorder: `record_chunk` Function

This project includes a utility function, `record_chunk`, to record a specific length of audio and save it as a WAV file. Below is a detailed explanation of how the function works and how to use it.

---

## Function Overview

### `record_chunk(p, stream, file_path, chunk_length=1)`

This function records a chunk of audio from a provided input stream and saves it to a specified file in WAV format.

### Parameters
- **`p`**: An instance of PyAudio, used to manage audio settings and formats.
- **`stream`**: An active audio input stream (e.g., from a microphone).
- **`file_path`**: The file path where the audio recording will be saved as a `.wav` file.
- **`chunk_length`**: The duration of the recording, in seconds (default is 1 second).

---

## How It Works
1. **Reads audio data**:
   - The function reads audio in chunks of 1024 frames until the specified `chunk_length` is reached.
   - The number of iterations is calculated based on the sample rate (16,000 Hz) and chunk size (1024 frames).

2. **Stores audio data**:
   - Audio data is temporarily stored in a list (`frames`), which holds each captured chunk.

3. **Configures the WAV file**:
   - The function sets the following parameters for the WAV file:
     - **Channels**: Mono (1 channel).
     - **Sample Width**: Configured for 16-bit audio (`paInt16`).
     - **Sample Rate**: 16 kHz, suitable for voice recording.

4. **Writes the audio to a file**:
   - Combines all recorded chunks and writes them to a WAV file at the specified `file_path`.

---

## Example Code
Below is an example of how to use the `record_chunk` function to record and save audio:

```python
import pyaudio
from your_module import record_chunk  # Replace 'your_module' with the actual module name

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream for audio input
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1024
)

# Record a 5-second audio chunk and save it to 'recording.wav'
record_chunk(p, stream, "recording.wav", chunk_length=5)

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()