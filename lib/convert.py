# Converts images into Minecraft particles mcfunction file.
# To use this, you would need python 3 and PIL.
# This tool is created by Red Cocoon. Please do not remove this line, please :'(
# Red Cocoon is the original author I jut modified this
import os
from PIL import Image
from moviepy.editor import *
import shutil
from lib.make_folders import make_resourcepack
from math import ceil

def normalize_color(color):
            new_color = []
            for i in range(4):
                new_color.append(color[i]/255)
            return new_color

def convert(array_images, total_frames, function_name, particles_density, datapack_location, fps, pos0):
    """
    array_images = array of frames
    total frames = like the name
    function_name = function name
    """
    index_ylyl = 0
    #output_path = f"{os.getcwd()}/particles-datapack/data/{function_name}/functions/src"
    print("Starting to convert frames")
    for current_image in array_images:
        index_ylyl = index_ylyl + 1
        command = "particleex normal minecraft:end_rod {0:.4f} {1:.4f} {2:.4f} {3:.3f} {4:.3f} {5:.3f} {6:.3f} 0.0 0.0 0.0 0 0 0 1 2"
        # This will produce 4096 particles in one frame, 64*64 = 4096 particles x*y
        particle_resolution = (64,64)
        particle_density = int(particles_density)
        image = Image.fromarray(current_image)
        image.thumbnail(particle_resolution)
        img_x, img_y = image.size
        rgba_img = image.convert('RGBA')
        
        particles = []
        if index_ylyl == 1:
            particles.insert(0, "tag @s add video_player")
        for i in range(img_x):
            for j in range(img_y):
                color = normalize_color(rgba_img.getpixel((i, j)))
                relative_x = float((img_x/2)-i)/particle_density
                relative_y = float((img_y/2)-j)/particle_density
                new_command = command.format(float(pos0[0]) + relative_x, float(pos0[1]), float(pos0[2]) + relative_y,color[2],color[1],color[0],color[3])
                particles.append(new_command)
            #with open(output_path + f"/{index_ylyl}.mcfunction", "w") as file:
        if index_ylyl+1 < len(array_images):
            particles.append(f"schedule function {function_name}:src/{index_ylyl+1} {ceil(20/fps)}t")
        else:
            particles.append("tag @a remove video_player")
        with open(f"{datapack_location}/data/{function_name}/functions/src/{index_ylyl}.mcfunction", "w") as file:
            for line in particles:
                file.write(line+"\n")
    shutil.make_archive(datapack_location, 'zip', os.path.join(os.getcwd(), 'result', 'particles_datapack'))
    print("Finished!")

def convert_audio(file_location, function_name, resourcepack_path):
    video_clip = VideoFileClip(file_location)
    has_audio = video_clip.audio is not None
    if has_audio:
        make_resourcepack(function_name, resourcepack_path)
        video_clip.audio.write_audiofile(os.path.join(resourcepack_path,'assets', 'minecraft', 'sounds', function_name+'_audio.ogg'))
        shutil.make_archive(resourcepack_path, 'zip', os.path.join(os.getcwd(), 'result', 'audio_packs'))
