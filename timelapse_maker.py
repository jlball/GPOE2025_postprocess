import argparse
from data import read_file, read_files
import os
import imageio.v2 as imageio

parser = argparse.ArgumentParser()  
parser.add_argument("dir", help="directory with hdf5 files")
parser.add_argument("--name", "-n", help="specific hdf5 file")
parser.add_argument("--fps", "-f", help="frames per second", default=24)
args = parser.parse_args()

os.chdir(args.dir)

if args.name is not None:
    timestamps, images = read_file(args.name, 'exposure')
else:
    timestamps, images = read_files(args.dir, 'exposures')

try:
    os.mkdir("timelapses")
except:
    pass

# for i, image in enumerate(images):
#     imageio.imwrite(f'images/exposure-{i}.jpg', image)

imageio.mimsave(f'timelapses/{args.name}.mov', images, fps=args.fps)
