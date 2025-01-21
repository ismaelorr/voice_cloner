import tkinter as tk
from tkinter import filedialog, messagebox
import os
from src.recorder import Recorder
from src.voice_cloner import VoiceCloner

class VoiceClonerGUI:
    def __init__(self):
        self.recorder = Recorder()
        self.voice_cloner = VoiceCloner()
        self.text_content = ""
        self.window = tk.Tk()
        self.window.title("Voice Cloner")
        self.window.geometry("500x550")
        self.window.resizable(False, False)
        self.duration_label = tk.Label(self.window, text="Record duration: (seconds):", font=("Arial", 12))
        self.duration_label.pack(pady=5)
        self.duration_slider = tk.Scale(self.window, from_=5, to=60, orient="horizontal", length=300)
        self.duration_slider.set(60)
        self.duration_slider.pack(pady=10)
        self.record_button = tk.Button(
            self.window,
            text="Record Audio",
            command=self.record_audio,
            width=30,
            height=2
        )
        self.record_button.pack(pady=10)
        self.text_entry = tk.Entry(self.window, font=("Arial", 12), width=40)
        self.text_entry.pack(pady=10)
        self.load_text_button = tk.Button(
            self.window,
            text="Charge txt",
            command=self.load_text_file,
            width=30,
            height=2
        )
        self.load_text_button.pack(pady=10)
        self.language_label = tk.Label(self.window, text="Select lenguage:", font=("Arial", 12))
        self.language_label.pack(pady=5)
        self.language_option = tk.StringVar(value="en")
        self.language_menu = tk.OptionMenu(self.window, self.language_option, "en", "fr")
        self.language_menu.pack(pady=10)
        self.generate_button = tk.Button(
            self.window,
            text="Generate audio with cloned voice",
            command=self.generate_audio,
            width=30,
            height=2
        )
        self.generate_button.pack(pady=10)
        self.message_label = tk.Label(self.window, text="State: Waiting interaction", font=("Arial", 12))
        self.message_label.pack(pady=10)

    def record_audio(self):
        duration = self.duration_slider.get()
        self.recorder.duration = duration
        try:
            self.recorder.record_audio()
            self.message_label.config(text=f"Record completed. Duration: {duration} seconds.")
        except Exception as e:
            messagebox.showerror("Error", f"Can't record audio.\n{e}")

    def load_text_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")],
            title="Select txt File"
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text_content = file.read()
                self.message_label.config(text="Text charged for archive")
                messagebox.showinfo("Text charged", "Text charged correctly.")
            except Exception as e:
                messagebox.showerror("Error", f"Can't charge the file.\n{e}")

    def generate_audio(self):
        if not self.text_content:
            self.text_content = self.text_entry.get()

        if not self.text_content.strip():
            messagebox.showerror("Error", "Please, ingress text for generate audio.")
            return
        voice_sample_path = "data/recorded_audio.wav"
        if not os.path.exists(voice_sample_path):
            messagebox.showerror("Error", "Don't find the audio")
            return
        try:
            output_path = "data/generated_audio.wav"
            language = self.language_option.get()
            self.voice_cloner.clone_voice(voice_sample_path, self.text_content, output_path, language=language)
            messagebox.showinfo("Audio generated succesfully", f"audio generated and saved in:\n{output_path}")
            self.message_label.config(text="Audio generated succesfully")
        except Exception as e:
            messagebox.showerror("Error", f"Can't generate audio\n{e}")

    def run(self):
        self.window.mainloop()
