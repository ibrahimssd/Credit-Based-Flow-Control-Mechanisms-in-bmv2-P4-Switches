import matplotlib.pyplot as plt
import os
import logging
# set up logger 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to the text file
file_paths = []
folder_path = f'basic_forwarding'
for file_name in os.listdir(folder_path):
    if file_name.endswith("60.txt"):
        logger.info(f'file: {file_name} ends with 60.txt')
        file_paths.append(os.path.join(folder_path, file_name))
    else:
        logger.info(f'file: {file_name} does not end with 60.txt')


for file in file_paths:
    print('processing file: ', file)
    # extract only  2 chars before .txt
    file_RTT = file[-6:-4]
    file_RTT = str(file_RTT)
    print('file_RTT: ', file_RTT)
    f = open(file, "r")
    lines = f.readlines()
    RTTs = []
    icmp_seq = []
    for x in lines:
        # result.append(x.split(' ')[1])
        line = x.split(' ')

        if line[0] == '64':
            # print('line: ', line)
            rtt = line[7][5:9]
            seq = line[5][9::]
            # if seq == '100':
            #     break
            # print('seq: ', seq)
            icmp_seq.append(int(seq))
            RTTs.append(float(rtt))
        # extract last line
        if line[0] == 'rtt':
            # extract whole line except the first character
            last_line = line[1::]
            # remove second element from the list
            last_line.pop(1)
            # remove \n from last element
            last_line[-1] = last_line[-1][:-1]
            # concatenate all elements in the list
            last_line = '_'.join(last_line)
    
    
    f.close()
    
    avg_rtt = sum(RTTs)/len(RTTs)
    print('avg_rtt: ', avg_rtt)
    # plot y vs x
    plt.plot(icmp_seq, RTTs)
    logger.info(f'last_line: {last_line}')
    # set title and x, y - axes labels
    # extract letters afte / and before .txt
    title = file.split('/')[-1]
    plt.title(title)
    plt.xlabel('icmp seq')
    plt.ylabel('rtt ms')
    # add coment on figure 
    plt.annotate(f'avg_rtt: {avg_rtt}', xy=(0.05, 0.95), xycoords='axes fraction')
    # legend
    plt.legend([f'RTT: {file_RTT} ms'])
    # save plot
    plt.savefig(f'./{folder_path}/plots/{title}_ms.png')
    logger.info(f'saved plot: {title}_ms.png in folder: {folder_path}/plots/')
    # show plot to user
    # plt.show()
    plt.close()
