import matplotlib.pyplot as plt
import logging
import os 
import numpy as np

#bandwidth = 1.05 Mbits/s
BANDWIDTH = 1.05 * 1000000

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# # Assuming file_paths is a list of file paths
# file_paths = ['path_to_file1.txt', 'path_to_file2.txt']  # Replace with your actual file paths
# folder_path = 'path_to_plots_folder'  # Replace with your actual folder path
file_paths = []
folder_path = f'basic_forwarding'
for file_name in os.listdir(folder_path):
    if file_name.endswith("60.txt"):
        logger.info(f'file: {file_name} ends with 60.txt')
        file_paths.append(os.path.join(folder_path, file_name))

    else:
        logger.info(f'file: {file_name} does not end with 60.txt')



# Data container for all RTTs
all_RTTs = []

for file in file_paths:
    print('Processing file:', file)
    
    # Extract RTT from the filename, assuming the naming convention holds
    file_RTT = file[-6:-4]
    print('File RTT:', file_RTT)
    
    with open(file, "r") as f:
        lines = f.readlines()
        RTTs = [float(line.split(' ')[7].split('=')[1]) for line in lines if line.startswith('64')]
        
        
        # Remove outliers
        RTTs = [x for x in RTTs if x < 80]
    
    all_RTTs.append(RTTs)  # Append the list of RTTs for this file to the main list

# compute BDP 
all_BDPs = []
for RTTs in all_RTTs:
    BDPs = [BANDWIDTH * rtt / 1000 for rtt in RTTs]
    all_BDPs.append(BDPs)

# Now that we have all RTTs, we can plot the box plots
plt.figure(figsize=(12, 8))
boxprops = dict(linestyle='-', linewidth=2, color='blue')
medianprops = dict(linestyle='-', linewidth=2, color='firebrick')
whiskerprops = dict(linestyle='--', linewidth=2, color='black')
capprops = dict(linestyle='-', linewidth=2, color='black')

# Create boxplot
bp = plt.boxplot(all_BDPs, patch_artist=True, boxprops=boxprops, medianprops=medianprops, 
                 whiskerprops=whiskerprops, capprops=capprops)



# Add scatter plots
for i in range(len(all_BDPs)):
    y = all_BDPs[i]
    x = np.random.normal(1+i, 0.04, size=len(y))
    plt.plot(x, y, 'r.', alpha=0.2)

# Add color to the boxes
for box in bp['boxes']:
    box.set_facecolor('lightblue')

plt.title('BDP for different Flows RTTs')
plt.xlabel('Flows')
plt.ylabel('BDP (bits)')

# Set the x-tick labels to file RTT values extracted from the filenames
plt.xticks(range(1, len(file_paths) + 1), ['FLOW1(h1->h2)', 'FLOW2(h3->h2)'])   

# Save and show the plot
plt.savefig(f'{folder_path}/plots/flows_box_plots.png')
logger.info('Saved combined box plot.')
plt.close()