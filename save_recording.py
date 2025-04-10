from obswebsocket import obsws, requests
import subprocess
import time
import os

host = 'localhost'
port = 4455
password = 'password'  # Change this to match your OBS WebSocket password

ws = obsws(host, port, password)
ws.connect()

try:
    while True:
        time.sleep(30)
        print("30 secs passed")
        time.sleep(30)
        print("30 secs passed")  # 1 minutes
        ws.call(requests.SaveReplayBuffer())
        print("Replay buffer saved!")

        folder_path = r"C:\Users\szive\Videos"  # Change this to your target folder

        # Get list of full file paths
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                 os.path.isfile(os.path.join(folder_path, f))]

        # Sort files by last modified time (newest first)
        sorted_files = sorted(files, key=os.path.getmtime, reverse=True)

        # Get the second newest file
        if len(sorted_files) >= 2:
            newest_file = sorted_files[1]
            print(f"Newest file: {newest_file}")  # C:\Users\szive\Videos\2025-04-05 08-44-20.mp4

            time.sleep(10)

            python_path = r'C:\Users\szive\PycharmProjects\HumanDetection\.venv\Scripts\python.exe'  # Full path to the Python where 'ultralytics' is installed
            subprocess.run([python_path, "main.py", newest_file])
        else:
            print("Not enough files in the folder.")
except KeyboardInterrupt:
    print("Stopped by user.")
    ws.disconnect()
