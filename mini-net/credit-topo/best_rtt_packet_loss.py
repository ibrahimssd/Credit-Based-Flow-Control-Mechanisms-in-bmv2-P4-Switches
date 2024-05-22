import matplotlib.pyplot as plt
import numpy as np 


# results_dictionary = {20:[(109,108),(103,102),(86,85),(140,139),(134,132)],40:[(64.6,63.8),(60.1,58.6),(72.4,69.7),(70.2,68.6),(58.4,57.6)],
# 50:[(48.7,47.4),(44.3,43.2),(39.9,39.4),(43.2,41.9),(41.5,39.8)], 60:[(45.8,43.9),(42.6,40.3),(40.5,39.0),(37.1,35.4),(41.8,40.8)],
# 100:[(32.7,31.5),(38.3,36.1),(38.6,36.9),(39.1,36.9),(28.4,27.5)]
#           }

# # calculate average of tuples for each RTT value
# for key in results_dictionary:
#     results_dictionary[key] = [sum(x)/len(x) for x in zip(*results_dictionary[key])]
    

# print('results_dictionary.values(): ', results_dictionary.values())

# # average list values for each RTT key
# for key in results_dictionary:
#     results_dictionary[key] = [sum(results_dictionary[key])/len(results_dictionary[key])]
    
    

# print('results_dictionary.values(): ', results_dictionary.values())


# # plot bar plot the results to compare values of RTT values  

# # set width of bar
# barWidth = 0.25

# # set height of bar
# bars1 = results_dictionary[20]
# bars2 = results_dictionary[40]
# bars3 = results_dictionary[50]
# bars4 = results_dictionary[60]
# bars5 = results_dictionary[100]

# # Set position of bar on X axis
# r1 = np.arange(len(bars1))
# r2 = [x + barWidth for x in r1]
# r3 = [x + barWidth for x in r2]
# r4 = [x + barWidth for x in r3]
# r5 = [x + barWidth for x in r4]
# # name x axis and y axis
# plt.xlabel('RTT values')
# plt.ylabel('Througput (Mbps)')

# # Make the plot
# plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, label='RTT 20 ms')
# plt.bar(r2, bars2, color='#5a7f2d', width=barWidth, edgecolor='white', label='RTT 40 ms')
# plt.bar(r3, bars3, color='blue', width=barWidth, edgecolor='white', label='RTT 50 ms')
# plt.bar(r4, bars4, color='#2daffe', width=barWidth, edgecolor='white', label='RTT 60 ms')
# plt.bar(r5, bars5, color='#2d1f5e', width=barWidth, edgecolor='white', label='RTT 100 ms')

# # Add xticks on the middle of the group bars
# # plt.xlabel('group', fontweight='bold') 
# # plt.xticks([r + barWidth for r in range(len(bars1))], ['min', 'avg', 'max', 'mdev'])
        
# # Create legend & Show graphic
# plt.legend()
# plt.show()

rtt20 = [0.3734733017058645, 0.46491969568892644, 0.21732538158293743, 0.2622887118709928]
rtt40 = [0.26322716504343247, 0.41425735738327435, 0.28771064529387586, 0.5270889138512054]
rtt50 =  [0.35737797423116713, 0.3495512517713746, 0.47249710261210665, 0.3332222592469177]
rtt60 = [0.2858832807570978, 0.2723146747352496, 0.6168831168831169, 0.3231723294610883]
rtt100 = [0.3830330543339481, 0.4092933670398459, 0.6804167552625984, 0.7039202945635694]
  
# # plot box plots for rtt values list 

# # Creating plot

# fig = plt.figure(figsize =(10, 7))
# # name y axis and x axis
# plt.ylabel('Packet loss rate')
# plt.xlabel('RTT values')
# # create box plot
# ax = fig.add_axes([0, 0, 1, 1])
# bp = ax.boxplot([rtt20, rtt40, rtt50, rtt60, rtt100] , patch_artist = True, labels = ['RTT 20 ms', 'RTT 40 ms', 'RTT 50 ms', 'RTT 60 ms', 'RTT 100 ms'])
# ax.set_xticklabels(['RTT 20 ms', 'RTT 40 ms', 'RTT 50 ms', 'RTT 60 ms', 'RTT 100 ms'], rotation=45)
#  # name boxes in box plot
# ax.set_title('Box plot of packet loss rate for different RTT values')
# # add names for each box plot
# # name each box plot
# colors = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink'] 
# for patch, color in zip(bp['boxes'], colors): 
#     patch.set_facecolor(color)

# # show plot
# plt.show()


fig = plt.figure(figsize =(10, 7))
# name y axis and x axis
plt.ylabel('Packet loss rate')
plt.xlabel('RTT values')
# create box plot
ax = fig.add_axes([0, 0, 1, 1])
bp = ax.boxplot([rtt20, rtt40, rtt50, rtt60, rtt100] , patch_artist = True, labels = ['RTT 20 ms', 'RTT 40 ms', 'RTT 50 ms', 'RTT 60 ms', 'RTT 100 ms'])
ax.set_xticklabels(['RTT 20 ms', 'RTT 40 ms', 'RTT 50 ms', 'RTT 60 ms', 'RTT 100 ms'], rotation=45)
# name boxes in box plot
ax.set_title('Box plot of packet loss rate for different RTT values')
# add names for each box plot
# name each box plot
colors = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink'] 
for patch, color in zip(bp['boxes'], colors): 
    patch.set_facecolor(color)

# add labels to each box plot
for i, line in enumerate(bp['medians']):
    # get x and y coordinates for the median line
    x, y = line.get_xydata()[1]
    # add text label with the RTT value
    ax.text(x, y, f"RTT value: {[20, 40, 50, 60, 100][i]} ms", verticalalignment='center')

# show plot
plt.show()

 














