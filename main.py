from pathlib import Path
import asyncio
import videoFragmentation
import videoMaker
import request
import time
import sys

# async def send_request(video_name):
#     await request.post(video_name)  # Ensure this is an async function

async def main():
    start_time = time.time()  # Start timer
    # arg = sys.argv[1]  # First argument passed in
    # print(f"Received argument: {arg}")
    # video_path = arg
    video_path = "test.mp4"
    frame_interval = 2

    output_folder = "sightings/extracted_frames"
    videoFragmentation.extract_frames_with_classes(video_path, output_folder, frame_interval)

    output_video = "00_output_video.mp4"
    frame_rate = 14

    folder_path = Path("sightings")
    # tasks = []  # Store tasks

    for folder in folder_path.iterdir():
        if folder.is_dir():
            folder_name = f"sightings/{folder.name}"
            video_name = videoMaker.make_video(folder_name, f"{folder_name}/{output_video}", frame_rate)

            await request.post(video_name)
            # # Schedule the request task
            # task = asyncio.create_task(send_request(video_name))
            # tasks.append(task)

    # await asyncio.gather(*tasks)  # Wait for all requests to finish

    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


# ✅ Correct way to call the async function in the script
if __name__ == "__main__":
    asyncio.run(main())
