import sounddevice as sd
import numpy as np
import whisper
import tempfile
import os
from pynput import keyboard


class WhisperTranscriber:
    def __init__(self, model_size="medium", sample_rate=16000):
        self.sample_rate = sample_rate
        self.model_size = model_size
        self.model = whisper.load_model(self.model_size)
        self.is_recording = False
        self.recording = []  # Para almacenar los datos grabados

    def on_press(self, key):
        if key == keyboard.Key.space and not self.is_recording:
            self.is_recording = True
            self.recording = []  # Resetea la grabación
            print("Recording started...")

    def on_release(self, key):
        if key == keyboard.Key.space and self.is_recording:
            self.is_recording = False
            print("Recording stopped.")
            return False  # Salir del listener

    def record_audio(self, duration=15):
        print("Hold the spacebar to start recording...")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while True:
                if self.is_recording:
                    # Grabar en chunks pequeños (streaming)
                    chunk = sd.rec(int(self.sample_rate * duration), samplerate=self.sample_rate, channels=1, dtype="int16")
                    sd.wait()  # Esperar a que el chunk termine
                    self.recording.append(chunk)
                else:
                    if len(self.recording) > 0:
                        break
            listener.join()

        # Combinar todos los chunks grabados
        full_recording = np.concatenate(self.recording, axis=0)
        return full_recording

    def save_temp_audio(self, recording, temp_path="temp/"):
        os.makedirs(temp_path, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=temp_path, delete=False, suffix=".wav") as temp_file:
            # Guardar la grabación directamente como WAV
            from scipy.io.wavfile import write
            write(temp_file.name, self.sample_rate, recording)
            return temp_file.name

    def transcribe_audio(self, file_path):
        print(f"Transcribing file: {file_path}")
        result = self.model.transcribe(file_path, language="es")
        print(f"Transcription: {result['text']}")
        os.remove(file_path)  # Limpiar archivo temporal
        return result['text']

    def run(self):
        try:
            while True:
                audio_data = self.record_audio()
                temp_audio_path = self.save_temp_audio(audio_data)
                transcription = self.transcribe_audio(temp_audio_path)
                print("\nPress the spacebar to record again, or Ctrl+C to exit.")
        except KeyboardInterrupt:
            print("Exiting...")
            return


if __name__ == "__main__":
    transcriber = WhisperTranscriber()
    transcriber.run()
