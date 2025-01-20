import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, savgol_filter
from scipy.interpolate import make_smoothing_spline

def plot_mag_curve(folder_name, ax, color="red", filter_kernel=15, camera_name=None, derivative=False): 
    files = [
            f'{folder_name}/{file}'
            for file in os.listdir(folder_name)
            if file[-3:] == 'txt' and "measurements" in file
        ]

    data = np.loadtxt(files[0])

    timestamps = data[1:, 0]
    bxs = data[1:, 2]
    bys = data[1:, 3]
    bzs = data[1:, 4]

    for file in files[1:]:
        data = np.loadtxt(file)
        timestamps = np.concatenate((timestamps, data[1:, 0]))
        bxs = np.concatenate((bxs, data[1:, 2]))
        bys = np.concatenate((bys, data[1:, 3]))
        bzs = np.concatenate((bzs, data[1:, 4]))

    sortidxs = np.argsort(timestamps)
    timestamps = timestamps[sortidxs]
    bxs = bxs[sortidxs]
    bys = bys[sortidxs]
    bzs = bzs[sortidxs]

    bxs -= bxs[0]
    bys -= bys[0]
    bzs -= bzs[0]

    b2s = np.array(bxs)**2 + np.array(bys)**2 + np.array(bzs)**2

    times_hrs = (timestamps - timestamps[0])/3600

    if camera_name is not None:
        label = camera_name
    else:
        label = folder_name

    if derivative:
        spline_fit_x = make_smoothing_spline(times_hrs, bxs, lam=4)
        spline_fit_y = make_smoothing_spline(times_hrs, bxs, lam=4)
        spline_fit_z = make_smoothing_spline(times_hrs, bxs, lam=4)


        # ax2 = ax.twinx()

        # ax2.step(times_hrs, 
        #     medfilt(temps, kernel_size=filter_kernel), 
        #     where='mid', 
        #     color='black')

        # ax2.plot(times_hrs,
        #     spline_fit(times_hrs), color="green")

    else:
        ax.step(times_hrs, 
            medfilt(bxs, kernel_size=filter_kernel), 
            where='mid', 
            label=label,
            color='red')
        ax.step(times_hrs, 
            medfilt(bys, kernel_size=filter_kernel), 
            where='mid', 
            label=label,
            color='blue')
        ax.step(times_hrs, 
            medfilt(bzs, kernel_size=filter_kernel), 
            where='mid', 
            label=label,
            color='green')
        ax.step(times_hrs, 
            medfilt(b2s, kernel_size=filter_kernel), 
            where='mid', 
            label=label,
            color='black')
        ax.set_ylabel('Field Strength (uT)')

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

    ax = plot_mag_curve(args.dir, ax, color="red", filter_kernel=args.filter_kernel)

    #plt.show()  # Add this line to render the plot

    fig.savefig(f'{args.output}/{args.output_name}', dpi=300)

    plt.show()


