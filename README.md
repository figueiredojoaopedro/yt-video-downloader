# yt-video-downloader

✦ To fix the FFmpeg error and include it in your
installer, follow these steps:

1. Download FFmpeg
   You need the FFmpeg executables (ffmpeg.exe and
   ffprobe.exe) in your project folder so I can bundle
   them.

- Download the "essentials" build from gyan.dev
  (https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essen
  tials.7z).
- Extract it and copy ffmpeg.exe and ffprobe.exe (from
  the bin folder) into:

C:\Users\defig\Documents\Projects\yt-video-downloader\

2. What I've already done:

- Updated main.py: Added logic to find FFmpeg inside  
  the bundled .exe using sys.\_MEIPASS.
- Updated main.spec: Configured PyInstaller to include
  ffmpeg.exe and ffprobe.exe inside your final  
  yt-video-downloader.exe.

3. Rebuild the App:
   Once you have placed the .exe files in the folder, run
   this command again to create the new bundle:
   1 python -m PyInstaller main.spec --noconfirm

4. Create the Installer:
   Now, when you run your Inno Setup script
   (installer_script.iss), the yt-video-downloader.exe it
   packages will already contain FFmpeg inside it. Your
   users won't need to install anything else!

Would you like me to try and download FFmpeg for you  
 via command line? (Note: You might need to install 7zip
or similar to extract it).
