import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, savgol_filter
from scipy.interpolate import make_smoothing_spline
import scipy.ndimage as nd

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

    b2s = np.sqrt(np.array(bxs)**2 + np.array(bys)**2 + np.array(bzs)**2)

    times_hrs = (timestamps - timestamps[0])/3600

    if camera_name is not None:
        label = camera_name
    else:
        label = folder_name

    lam = 1e-6
    spline_fit_x = (make_smoothing_spline(times_hrs, nd.median_filter(bxs, 5), lam=lam)(times_hrs))
    spline_fit_y = (make_smoothing_spline(times_hrs, nd.median_filter(bys, 5), lam=lam)(times_hrs))
    spline_fit_z = (make_smoothing_spline(times_hrs, nd.median_filter(bzs, 5), lam=lam)(times_hrs))

    dxdt = nd.median_filter(np.gradient(spline_fit_x), 5)
    dydt = nd.median_filter(np.gradient(spline_fit_y), 5)
    dzdt = nd.median_filter(np.gradient(spline_fit_z), 5)

    ax[1].step(times_hrs, 
        dxdt,
        where='mid', 
        label=label,
        color='red')
    ax[1].step(times_hrs, 
        dydt,
        where='mid', 
        label=label,
        color='blue')
    ax[1].step(times_hrs, 
        dzdt,
        where='mid', 
        label=label,
        color='green')
    
    ax[1].set_ylabel('Field Strength Change (uT/step)')


    # ax2 = ax.twinx()

    # ax2.step(times_hrs, 
    #     medfilt(temps, kernel_size=filter_kernel), 
    #     where='mid', 
    #     color='black')

    # ax2.plot(times_hrs,
    #     spline_fit(times_hrs), color="green")

    ax[0].step(times_hrs, 
        medfilt(bxs, kernel_size=filter_kernel), 
        where='mid', 
        label=label,
        color='red', 
        alpha = .1)
    ax[0].step(times_hrs, 
        medfilt(bys, kernel_size=filter_kernel), 
        where='mid', 
        label=label,
        color='blue', 
        alpha = .1)
    ax[0].step(times_hrs, 
        medfilt(bzs, kernel_size=filter_kernel), 
        where='mid', 
        label=label,
        color='green', 
        alpha =.1)
    ax[0].step(times_hrs, 
        medfilt(b2s, kernel_size=filter_kernel), 
        where='mid', 
        label=label,
        color='black', 
        alpha = .1)

    ax[0].step(times_hrs, 
        spline_fit_x,
        where='mid', 
        label=label,
        color='red')
    ax[0].step(times_hrs, 
        spline_fit_y,
        where='mid', 
        label=label,
        color='blue')
    ax[0].step(times_hrs, 
        spline_fit_z,
        where='mid', 
        label=label,
        color='green')
    ax[0].set_ylabel('Field Strength (uT)')

    ax[1].set_xlabel('Time (hrs)')
    ax[1].set_xbound(0, times_hrs[-1])

    return ax

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="directory with measurement files to load")
    parser.add_argument("--filter_kernel", help="size of median filter kernel", type=int, default=15)
    parser.add_argument("--output", help="output directory", default='.')
    parser.add_argument("--output_name", help="output name", default='temperature.png')
    args = parser.parse_args()

    fig, ax = plt.subplots(2, sharex = True)
    ax[0].grid()
    ax[1].grid()
    plt.subplots_adjust(wspace=0, hspace=0)

    ax = plot_mag_curve(args.dir, ax, color="red", filter_kernel=args.filter_kernel,derivative = True)

    #plt.show()  # Add this line to render the plot

    fig.savefig(f'{args.output}/{args.output_name}', dpi=300)

    plt.show()


