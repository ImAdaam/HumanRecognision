import os
import cv2
from ultralytics.engine.results import Results
import threading

class Sighting:
    def __init__(self, frames_before, sighting, frames_after, number, folder, frames_to_save=60):
        self.frames_before = frames_before
        self.frames_after = frames_after
        self.frames_to_save = frames_to_save
        self.frames_to_save_before = frames_to_save
        self.sighting = sighting
        self.frames_to_save_after = frames_to_save
        self.frames_to_save = frames_to_save
        self.number = number
        self.folder = folder
        self.sightings_count = 0

    def add_frame_before(self, frame):
        if self.sightings_count < 1:
            if len(self.frames_before) > self.frames_to_save:
                self.frames_before.pop(0)
            self.frames_before.append(frame)
            self.frames_to_save_before -= 1
        else:
            if self.frames_to_save_before > 0:
                self.frames_before.append(frame)
                self.frames_to_save_before -= 1

    def add_frame_array_before(self, array):
        if self.sightings_count < 1:
            if len(self.frames_before) + len(array) > self.frames_to_save:
                self.frames_before.extend(array)
                self.frames_before = self.frames_before[len(self.frames_before) - self.frames_to_save:]
                self.frames_to_save_before = 0
            else:
                self.frames_before.extend(array)
                self.frames_to_save_before -= len(array)
        else:
            if self.frames_to_save_before > 0:
                array = array[:len(self.frames_before) - len(array)]
                self.frames_before.extend(array)
                self.frames_to_save_before = 0

    def add_sighting(self, frame):
        self.sighting.append(frame)
        self.sightings_count += 1
        if self.frames_to_save_after < self.frames_to_save:
            self.reset_frames_to_save()

    def add_frame_after(self, frame):
        if self.frames_to_save_after > 1:
            self.frames_after.append(frame)
            self.frames_to_save_after -= 1

    def needs_after_frames(self):
        return self.frames_to_save_after > 0

    def needs_after_before(self):
        return self.frames_to_save_before > 0
    
    def reset_frames_to_save(self):
        self.frames_to_save_after = self.frames_to_save
        self.sighting.extend(self.frames_after)
        self.frames_after = []

    def save_frames(self):
        self.folder = self.folder + '_' + str(self.number)
        os.makedirs(self.folder, exist_ok=True)

        # TODO: have to wait for each other
        # t1 = threading.Thread(target=self.save_prev_frames())
        # t2 = threading.Thread(target=self.save_sighting_frames())
        # t3 = threading.Thread(target=self.save_after_frames())
        #
        # t1.start()
        # t2.start()
        # t3.start()

        self.save_prev_frames()
        self.save_sighting_frames()
        self.save_after_frames()


    def save_prev_frames(self):
        for _id, _frame in enumerate(self.frames_before):
            frame_filename = os.path.join(self.folder, f"frame_prev_{_id}.jpg")
            cv2.imwrite(frame_filename, _frame)

    def save_sighting_frames(self):
        for _id, _frame in enumerate(self.sighting):
            frame_filename = os.path.join(self.folder + '/', f"frame_{_id:04d}.jpg")
            if isinstance(_frame, Results):
                _frame = _frame.plot()  # Extracts an image (NumPy array) with detections
            cv2.imwrite(frame_filename, _frame)

    def save_after_frames(self):
        for _id, _frame in enumerate(self.frames_after):
            frame_filename = os.path.join(self.folder, f"frame_after_{_id}.jpg")
            cv2.imwrite(frame_filename, _frame)