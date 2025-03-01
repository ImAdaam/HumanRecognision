import cv2
import os
import imageDetection

def extract_frames(video_path, output_folder, frame_interval=1):
    """
    Extract frames from a video and save them as images.

    :param video_path: Path to the input video file
    :param output_folder: Folder where extracted frames will be saved
    :param frame_interval: Extract every nth frame (default is 1, meaning extract every frame)
    """

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 0
    saved_count = 0

    sightings = 0
    sightings_continuous = False
    frames_to_save_after_sighting = 60
    frames_before_sighting = []
    frames_after_sighting = []

    while True:
        success, frame = cap.read()

        if not success:
            break  # End of video

        # Save every nth frame
        if frame_count % frame_interval == 0:
            observe = imageDetection.analyse(frame)
            if len(frames_before_sighting) > 60:
                frames_before_sighting.pop(0)
            frames_before_sighting.append(frame)

            # Save sightings
            # TODO: move this to true condition if frames_before is not directly saved
            if sightings_continuous:
                out_folder = output_folder + '_' + str(sightings)
            else:
                out_folder = output_folder + '_' + str(sightings + 1)
            os.makedirs(out_folder, exist_ok=True)

            if observe:
                for _frame,_id in enumerate(frames_before_sighting):
                    frame_filename = os.path.join(out_folder, f"frame_prev_{_id}.jpg")
                    cv2.imwrite(frame_filename, _frame)

                frame_filename = os.path.join(out_folder, f"frame_{saved_count:04d}.jpg")
                cv2.imwrite(frame_filename, frame)

                # Increment variables
                saved_count += 1
                sightings_continuous = True
                frames_to_save_after_sighting = 60
            else:
                # Todo: save frames to frames_after_sighting for every sightings
                #  now: stops after new sighting
                #       directly saves to folders
                if frames_to_save_after_sighting > 0:
                    out_folder = output_folder + '_' + str(sightings)
                    frame_filename = os.path.join(out_folder, f"frame_{saved_count:04d}.jpg")
                    cv2.imwrite(frame_filename, frame)
                    frames_to_save_after_sighting -= 1
                if sightings_continuous:
                    sightings += 1
                    sightings_continuous = False
                else:
                    sightings_continuous = False

        frame_count += 1

    cap.release()
    print(f"Extraction complete! {saved_count} frames saved in '{output_folder}'.")

def extract_frames_with_boxes(video_path, output_folder, frame_interval=1):
    """
    Extract frames from a video and save them as images.

    :param video_path: Path to the input video file
    :param output_folder: Folder where extracted frames will be saved
    :param frame_interval: Extract every nth frame (default is 1, meaning extract every frame)
    """

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # TODO: maybe put to class variable -> other thread can access the images
    frame_count = 0
    saved_count = 0

    sightings = 0
    sightings_continuous = False
    frames_to_save_after_sighting = 60
    frames_before_sighting = [] # TODO: thread pulls out first -> save -> delete
    frames_after_sighting = []# TODO: thread pulls out first -> save -> delete

    while True:
        success, frame = cap.read()

        if not success:
            break  # End of video

        # Save every nth frame
        if frame_count % frame_interval == 0:
            observe, boxed_frame = imageDetection.analyse_with_return(frame)
            if len(frames_before_sighting) > 60:
                frames_before_sighting.pop(0)
            frames_before_sighting.append(boxed_frame)

            # Save sightings
            # TODO: move this to true condition if frames_before is not directly saved
            if sightings_continuous:
                out_folder = output_folder + '_' + str(sightings)
            else:
                out_folder = output_folder + '_' + str(sightings + 1)
            os.makedirs(out_folder, exist_ok=True)

            if observe:
                # TODO: image saving to different thread -> same image saving on multiple places
                for _frame,_id in enumerate(frames_before_sighting):
                    frame_filename = os.path.join(out_folder, f"frame_prev_{_id}.jpg")
                    cv2.imwrite(frame_filename, _frame)

                frame_filename = os.path.join(out_folder+'/', f"frame_{saved_count:04d}.jpg")
                boxed_frame = boxed_frame.plot()  # Extracts an image (NumPy array) with detections
                cv2.imwrite(frame_filename, boxed_frame)
                # boxed_frame.show()

                # Increment variables
                saved_count += 1
                sightings_continuous = True
                frames_to_save_after_sighting = 60
            else:
                # Todo: save frames to frames_after_sighting for every sightings
                #  now: stops after new sighting
                #       directly saves to folders
                if frames_to_save_after_sighting > 0:
                    out_folder = output_folder + '_' + str(sightings)
                    frame_filename = os.path.join(out_folder+'/', f"frame_{saved_count:04d}.jpg")
                    cv2.imwrite(frame_filename, frame)
                    frames_to_save_after_sighting -= 1
                if sightings_continuous:
                    sightings += 1
                    sightings_continuous = False
                else:
                    sightings_continuous = False

        frame_count += 1

    cap.release()
    print(f"Extraction complete! {saved_count} frames saved in '{output_folder}'.")