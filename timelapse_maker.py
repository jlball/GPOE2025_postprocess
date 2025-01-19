import argparse
from data import read_file, read_files
import os
import imageio.v2 as imageio
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import progressbar as pb
import numpy as np
from multiprocessing import Pool

parser = argparse.ArgumentParser()  
parser.add_argument("dir", help="directory with hdf5 files")
parser.add_argument("--name", "-n", help="output file name")
parser.add_argument("--fps", "-f", help="frames per second", default=24)
parser.add_argument("--timestamp", "-ts", help="draw timestamp on each video frame", action="store_true")
parser.add_argument("--resize", "-r", help="resize images to this height", type=int)
parser.add_argument("--font_size", "-fs", help="font size for timestamp", type=int, default=48)
parser.add_argument("--camera_name", "-cn", help="camera name to display on video")
parser.add_argument("--output_dir", "-o", help="output directory for video", default="timelapses")
parser.add_argument("--multiprocessing", "-mp", help="use multiprocessing", action="store_true")
args = parser.parse_args()

# Function which is used to process an individual frames
def process_image(i):
    pil_image = Image.fromarray(images[i])

    if args.resize is not None:
        pil_image = pil_image.resize(new_size)

    if args.timestamp:
        draw = ImageDraw.Draw(pil_image)
        text = datetimes[i].strftime('%Y-%m-%d %H:%M:%S')
        draw.text((10, 10), text, font=font, fill="white")

    if args.camera_name is not None:
        if not args.timestamp:
            draw = ImageDraw.Draw(pil_image)

        text = args.camera_name
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        position = (25, pil_image.height - text_height - 25)
        draw.text(position, text, font=font, fill="white")

    return np.array(pil_image)

# Get a list of all HDF5 files in the specified directory.
files = [
        f'{args.dir}/{file}'
        for file in os.listdir(args.dir)
        if file[-4:] == 'hdf5' and "exposures" in file
    ]

# Loop through each file and create a timelapse out of it
for i, file in enumerate(files):
    print("Loading image data...")
    timestamps, images = read_file(file, 'exposure')
    print("Finished loading image data.")

    datetimes = [datetime.fromtimestamp(ts) for ts in timestamps]

    # Setup based on selected options
    processed_images = []

    if args.resize is not None:
        width = np.floor(images.shape[2] * (args.resize/images.shape[1]))
        new_size = (int(width), args.resize)

    font = ImageFont.truetype("Arial.ttf",args.font_size)

    bar = pb.ProgressBar(max_value=len(images))

    # Loop through all images and apply selected processing steps
    if args.multiprocessing:
        print("Using multiprocessing...")
        with Pool() as pool:
            for result in bar(pool.imap(process_image, range(len(images)))):
                processed_images.append(result)

    else:
        for i, image in enumerate(bar(images)):
            processed_images.append(process_image(i))

    images = np.array(processed_images)

    if args.output_dir == "timelapses" and args.camera_name is not None:
        output_dir = args.camera_name
    else:
        output_dir = args.output_dir

    try:
        os.mkdir(output_dir)
    except:
        pass

    imageio.mimsave(f'{output_dir}/{args.name}_{i}.mov', images, fps=float(args.fps))
