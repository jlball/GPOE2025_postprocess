import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, savgol_filter

def plot_temp_curve(folder_name, ax, color="red", filter_kernel=15, camera_name=None, derivative=False): 
    files = [
            f'{folder_name}/{file}'
            for file in os.listdir(folder_name)
            if file[-3:] == 'txt' and "measurements" in file
        ]

    data = np.loadtxt(files[0])

    timestamps = data[1:, 0]
    temps = data[1:, 1]

    for file in files[1:]:
        data = np.loadtxt(file)
        timestamps = np.concatenate((timestamps, data[1:, 0]))
        temps = np.concatenate((temps, data[1:, 1]))

    sortidxs = np.argsort(timestamps)
    timestamps = timestamps[sortidxs]
    temps = temps[sortidxs]

    times_hrs = (timestamps - timestamps[0])/3600

    if camera_name is not None:
        label = camera_name
    else:
        label = folder_name

    if derivative:
        ax.plot(times_hrs, 
            np.gradient(medfilt(temps, kernel_size=filter_kernel), times_hrs),
            label=label,
            color=color)
        ax.set_ylabel('Temperature rate of change (C/hr)')

    else:
        ax.step(times_hrs, 
            medfilt(temps, kernel_size=filter_kernel), 
            where='mid', 
            label=label,
            color=color)
        ax.set_ylabel('Temperature (C)')

    ax.set_xlabel('Time (hrs)')
    ax.set_xbound(0, times_hrs[-1])

    return ax

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="directory with measurement files to load")
    parser.add_argument("--filter_kernel", help="size of median filter kernel", type=int, default=15)
    parser.add_argument("--output", help="output directory", default='.')
    parser.add_argument("--output_name", help="output name", default='temperature.png')
    args = parser.parse_args()

    fig, ax = plt.subplots()

    ax = plot_temp_curve(args.dir, ax, color="red", filter_kernel=args.filter_kernel)

    #plt.show()  # Add this line to render the plot

    fig.savefig(f'{args.output}/{args.output_name}', dpi=300)



