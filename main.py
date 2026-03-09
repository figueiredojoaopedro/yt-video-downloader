import customtkinter as ctk
import yt_dlp
import threading
import os
import sys
from tkinter import filedialog, messagebox

# Set appearance and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JPF YouTube Downloader")
        self.geometry("600x400")

        # Configure layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # UI Elements
        self.label = ctk.CTkLabel(self, text="YouTube Video Downloader", font=("Roboto", 24))
        self.label.grid(row=0, column=0, pady=20)

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Paste YouTube URL here...", width=500)
        self.url_entry.grid(row=1, column=0, padx=20, pady=10)

        # Options Frame
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=2, column=0, padx=20, pady=10)

        self.quality_label = ctk.CTkLabel(self.options_frame, text="Quality:")
        self.quality_label.grid(row=0, column=0, padx=10, pady=5)
        self.quality_var = ctk.StringVar(value="Best")
        self.quality_option = ctk.CTkOptionMenu(self.options_frame, variable=self.quality_var, 
                                              values=["Best", "1080p", "720p", "480p", "360p"])
        self.quality_option.grid(row=0, column=1, padx=10, pady=5)

        self.format_label = ctk.CTkLabel(self.options_frame, text="Format:")
        self.format_label.grid(row=0, column=2, padx=10, pady=5)
        self.format_var = ctk.StringVar(value="MP4")
        self.format_option = ctk.CTkOptionMenu(self.options_frame, variable=self.format_var, 
                                             values=["MP4", "MKV", "MP3"])
        self.format_option.grid(row=0, column=3, padx=10, pady=5)

        self.download_btn = ctk.CTkButton(self, text="Download", command=self.start_download)
        self.download_btn.grid(row=3, column=0, pady=10)

        self.progress_label = ctk.CTkLabel(self, text="Progress: 0%")
        self.progress_label.grid(row=4, column=0)

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=5, column=0, pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=6, column=0, pady=10)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # Calculate percentage
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            
            if total > 0:
                percent = downloaded / total
                # Use after() to update UI from thread safely
                self.after(0, self.update_progress, percent)
        
        elif d['status'] == 'finished':
            self.after(0, self.update_progress, 1.0)
            self.after(0, lambda: self.status_label.configure(text="Download Complete!", text_color="green"))

    def update_progress(self, percent):
        self.progress_bar.set(percent)
        self.progress_label.configure(text=f"Progress: {int(percent * 100)}%")

    def download_video(self, url, save_path, quality, file_format):
        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': resource_path('ffmpeg.exe') if sys.platform == 'win32' else resource_path('ffmpeg')
        }

        if file_format == "MP3":
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            # Video settings
            res_map = {
                "1080p": "1080",
                "720p": "720",
                "480p": "480",
                "360p": "360"
            }
            
            if quality == "Best":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
            else:
                res = res_map.get(quality, "720")
                ydl_opts['format'] = f'bestvideo[height<={res}]+bestaudio/best[height<={res}]'
            
            ydl_opts['merge_output_format'] = file_format.lower()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: self.status_label.configure(text=f"Error: {error_msg[:50]}...", text_color="red"))
            self.after(0, lambda m=error_msg: messagebox.showerror("Error", f"Failed to download: {m}"))
        finally:
            self.after(0, lambda: self.download_btn.configure(state="normal"))

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a valid YouTube URL.")
            return

        quality = self.quality_var.get()
        file_format = self.format_var.get()

        save_path = filedialog.askdirectory()
        if not save_path:
            return

        self.download_btn.configure(state="disabled")
        self.status_label.configure(text="Starting download...", text_color="white")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Progress: 0%")

        # Run download in a separate thread to keep UI responsive
        download_thread = threading.Thread(target=self.download_video, args=(url, save_path, quality, file_format), daemon=True)
        download_thread.start()

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()
