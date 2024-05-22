import tkinter
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import os
import logging
# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Path to the text file
file_paths = []
# iterate over folder files and plot the bitrate over time
# folder_path = f'iperf_basic_forwarding'
folder_path  = f'iperf_credit'
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt"):
        file_paths.append(os.path.join(folder_path, file_name))

for file_path in file_paths:
    # Lists to store the time intervals and bitrates
    intervals = []
    bitrates = []
    # Read the file and extract the relevant data
    with open(file_path, "r") as file:
        for line in file:
            if "sec" in line and "sender" not in line and "receiver" not in line:
                data = line.strip().split()
                bitrate = float(data[6])
                interval_str = data[2]
                start_time, end_time = interval_str.split('-')
                end_time = end_time.split('.')[0]
                interval = float(end_time)
                intervals.append(interval)
                bitrates.append(bitrate)

    logger.info(f'file: {file_path} intervals: {intervals}')
    logger.info(f'file: {file_path} bitrates: {bitrates}')
    # extract chars after / in file path
    title = file_path.split('/')[-1]
    # Plot the bitrate over time
    plt.plot(intervals, bitrates)
    plt.xlabel("Time (sec)")
    plt.ylabel("Bitrate (Mbits/sec)")
    # show average bitrate in the plot
    avg_bitrate = sum(bitrates) / len(bitrates)
    plt.axhline(y=avg_bitrate, color='r', linestyle='-', label='Average Bitrate')
    # show value of average bitrate
    plt.text(0, avg_bitrate, str(round(avg_bitrate, 2)), color='r')
    # show the max bitrate in the plot
    max_bitrate = max(bitrates)
    plt.axhline(y=max_bitrate, color='g', linestyle='-', label='Max Bitrate')
    # show value of max bitrate
    plt.text(0, max_bitrate, str(round(max_bitrate, 2)), color='g')
    plt.legend()
    plt.title("Bitrate Over Time for " + title)
    plt.grid(True)
    # save plot
    plt.savefig(f'./{folder_path}/plots/{title}.png')
    plt.show()
