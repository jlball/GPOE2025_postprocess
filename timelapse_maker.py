import argparse
from data import read_file
import os
import imageio.v2 as imageio

parser = argparse.ArgumentParser()  
parser.add_argument("dir", help="directory with hdf5 files")
parser.add_argument("name", help="specific hdf5 file")
args = parser.parse_args()

os.chdir(args.dir)

timestamps, images = read_file(args.name, 'exposure')

try:
    os.mkdir("timelapses")
except:
    pass

# for i, image in enumerate(images):
#     imageio.imwrite(f'images/exposure-{i}.jpg', image)

imageio.mimsave(f'timelapses/{args.name}.mov', images, fps=24)
