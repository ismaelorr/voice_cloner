from TTS.api import TTS

class VoiceCloner:
    def __init__(self, model_name="tts_models/multilingual/multi-dataset/your_tts"):
        print("Charging model...")
        self.model = TTS(model_name)

    def clone_voice(self, voice_sample_path, text, output_path="data/generated_audio.wav", language="en"):
        if not voice_sample_path:
            raise FileNotFoundError(f"We can't get sample {voice_sample_path}")

        print(f"Generating audio in {language}...")
        self.model.tts_to_file(text=text, speaker_wav=voice_sample_path, language=language, file_path=output_path)
        print(f"Audio saved in {output_path}")
