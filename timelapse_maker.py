import argparse
from data import read_file, read_files
import os
import imageio.v2 as imageio
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import progressbar as pb
import numpy as np

parser = argparse.ArgumentParser()  
parser.add_argument("dir", help="directory with hdf5 files")
parser.add_argument("--name", "-n", help="output file name")
parser.add_argument("--fps", "-f", help="frames per second", default=24)
parser.add_argument("--timestamp", "-ts", help="draw timestamp on each video frame", action="store_true")
parser.add_argument("--resize", "-r", help="resize images to this height", type=int)
parser.add_argument("--font_size", "-fs", help="font size for timestamp", type=int, default=48)
args = parser.parse_args()

timestamps, images = read_files(args.dir, 'exposures')
print("Finished loading image data...")

#images = images[:, :, 7:-7, :]

datetimes = [datetime.fromtimestamp(ts) for ts in timestamps]

# Setup based on selected options
processed_images = []

if args.resize is not None:
    width = np.floor(images.shape[2] * (args.resize/images.shape[1]))
    new_size = (int(width), args.resize)

if args.timestamp:
    font = ImageFont.truetype("Arial.ttf",args.font_size)

# Initialize progress bar
bar = pb.ProgressBar(max_value=len(images))

# Loop through all images and apply selected processing steps
for i, image in enumerate(bar(images)):
    pil_image = Image.fromarray(image)

    if args.resize is not None:
        pil_image = pil_image.resize(new_size)

    if args.timestamp:
        draw = ImageDraw.Draw(pil_image)
        text = datetimes[i].strftime('%Y-%m-%d %H:%M:%S')
        draw.text((10, 10), text, font=font, fill="white")
        
    processed_images.append(np.array(pil_image))

images = np.array(processed_images)

try:
    os.mkdir("timelapses")
except:
    pass

imageio.mimsave(f'timelapses/{args.name}.mov', images, fps=args.fps)
