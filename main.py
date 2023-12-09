import tkinter as tk
import tkinter.filedialog
import cv2
import os
from lib.main import main
import inquirer, re  
from termcolor import colored

#ask vid location
filetypes = (('MP4 files', '*.MP4'),)
root = tk.Tk()
filelocation = tk.filedialog.askopenfilename(title='Select a video file to convert',filetypes=filetypes)
root.destroy()
if(filelocation == ""):
    raise Exception("No video file")
print(filelocation)
video = cv2.VideoCapture(filelocation)
fps = video.get(cv2.CAP_PROP_FPS)
print("Current frame per second is %d. If fps is larger than 20, it will be adjusted to 20." % fps)
questions = [inquirer.Text('particles-density', message="Please Write the particles density",validate=lambda _, x: re.match('^[0-9]*$', x), default=5), 
             inquirer.Text('x', message="Please Write x0",validate=lambda _, x: re.match('^[0-9]*$', x), default=0),
             inquirer.Text('y', message="Please Write y0",validate=lambda _, x: re.match('^[0-9]*$', x), default=0),
             inquirer.Text('z', message="Please Write z0",validate=lambda _, x: re.match('^[0-9]*$', x), default=0),
             inquirer.Text('skip', message="Please Write How much Frames you want to skip (If 1, default fps applied)",validate=lambda _, x: re.match('^[0-9]*$', x), default=1),
             inquirer.Text('resol', message="Resolution (maximum NxN particles will be used for each frame, Default N = 64)",validate=lambda _, x: re.match('^[0-9]*$', x), default=64)]
inqanswers = inquirer.prompt(questions)
# convert frames
frames = []
os.system('cls' if os.name == 'nt' else 'clear')
print("Getting Frames")
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
for frame_number in range(total_frames):
    try:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()
        if not ret:
            raise Exception("Can't read frames")
        frames.append((frame))
    except Exception as e:
        raise Exception("An error occurred:", str(e))
print("Finished Extracting frames, Now converting into a MC Function")
main(frames, total_frames, inqanswers, filelocation, fps)
#main(inqanswers, inqanswers, inqanswers)
