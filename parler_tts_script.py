import librosa
import soundfile as sf

# Load the original audio file
y, sr = librosa.load("input_audio.wav", sr=22050)

# Modify pitch (+4 semitones increases pitch, -4 semitones lowers pitch)
y_high_pitch = librosa.effects.pitch_shift(y, sr=sr, n_steps=4)
y_low_pitch = librosa.effects.pitch_shift(y, sr=sr, n_steps=-4)

# Save the modified audio
sf.write("output_high_pitch.wav", y_high_pitch, sr)
sf.write("output_low_pitch.wav", y_low_pitch, sr)
