import yt_dlp as ydl
import os
import tempfile
import librosa
import noisereduce as nr
import soundfile as sf
import subprocess

def download_and_extract_audio(url, start_time, end_time, output_path):
    try:
        # Create a temporary directory to store the video file
        temp_dir = tempfile.mkdtemp()

        # Download the video using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, 'downloaded_video.%(ext)s'),  # Automatically handles extensions
        }

        with ydl.YoutubeDL(ydl_opts) as ydl_instance:
            ydl_instance.download([url])

        # Find the downloaded video/audio file
        downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith(('.mp4', '.webm'))]
        if not downloaded_files:
            raise FileNotFoundError("No video/audio file downloaded.")
        
        video_path = os.path.join(temp_dir, downloaded_files[0])  # Take the first valid file
        audio_path = os.path.join(temp_dir, "extracted_audio.wav")

        # Extract audio using ffmpeg
        subprocess.run([
            "ffmpeg", "-i", video_path, "-ss", str(start_time), "-to", str(end_time),
            "-ac", "1", "-ar", "16000", "-vn", audio_path
        ], check=True)

        # Load audio for noise reduction
        y, sr = librosa.load(audio_path, sr=None)

        # Apply noise reduction
        reduced_noise = nr.reduce_noise(y=y, sr=sr, prop_decrease=0.8)

        # Save the cleaned audio
        sf.write(output_path, reduced_noise, sr)

        # Clean up temporary files
        os.remove(video_path)
        os.remove(audio_path)

        print(f"Saved cleaned audio: {output_path}")

    except Exception as e:
        print(f"Error processing {url}: {e}")

# Example usage
youtube_url = "https://youtu.be/kTw_KyXcHIc?list=PLosaC3gb0kGBD6RKl3GJx329zdaGPF-fZ"
start_time = 31  # in seconds
end_time = 41 # in seconds
output_audio_path = "/mnt/32mins/aditi_processed/audio_generation/english/female_6.wav"

download_and_extract_audio(youtube_url, start_time, end_time, output_audio_path)
