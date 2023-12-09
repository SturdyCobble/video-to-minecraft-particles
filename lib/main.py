from termcolor import colored
import os
from moviepy.editor import *
from lib.convert import convert, convert_audio
from lib.make_folders import make_datapack
datapack_location = os.path.join(os.getcwd(), 'result', 'particles_datapack')
resourcepack_location = os.path.join(os.getcwd(), 'result', 'audio_packs')
def main(frames, total_frames, question_answer, filelocation, fps):
    os.system('cls' if os.name == 'nt' else 'clear')
    function_name = "particles" #question_answer['function-name']
    make_datapack(function_name, datapack_location)
    pos0 = (question_answer['x'], question_answer['y'], question_answer['z'])
    convert(frames, total_frames, function_name, question_answer['particles-density'], datapack_location, fps, pos0)
    convert_audio(filelocation, function_name, resourcepack_location)
    os.system('cls' if os.name == 'nt' else 'clear')
    
