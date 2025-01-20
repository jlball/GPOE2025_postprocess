from plot_temperature import plot_temp_curve
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory with measurement files to load")
parser.add_argument("--filter_kernel", help="size of median filter kernel", type=int, default=17)
parser.add_argument("--output", help="output directory", default='.')
parser.add_argument("--output_name", help="output name", default='mult_temps.png')
parser.add_argument("--derivative", "-d", help="plot derivative of temperatures", action='store_true')

args = parser.parse_args()

cameras = ["camel", "hedgehogigrade", "petrel", "axolotl", ]

fig, ax = plt.subplots()

norm = Normalize(vmin=0, vmax=len(cameras))

if args.derivative:
    for i, camera in enumerate(cameras):
        print(f"Looking in {args.dir}/{camera}")
        ax = plot_temp_curve(f'{args.dir}/{camera}', 
            ax, 
            color=cm.magma(norm(i)), 
            filter_kernel=args.filter_kernel,
            camera_name=camera,
            derivative=True)

    ax.set_ybound(lower=-10, upper=10)
else:
    for i, camera in enumerate(cameras):
        print(f"Looking in {args.dir}/{camera}")
        ax = plot_temp_curve(f'{args.dir}/{camera}', 
            ax, 
            color=cm.magma(norm(i)), 
            filter_kernel=args.filter_kernel,
            camera_name=camera)

ax.legend()
fig.savefig(f'{args.output}/{args.output_name}', dpi=300)