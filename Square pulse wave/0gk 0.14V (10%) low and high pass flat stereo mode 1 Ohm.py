import csv
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

x = []
x1 = []
x2 = []
curv10pc_y = []
resv10pc_y = []
priv10pc_y = []
resv10pc_y1 = []
resv10pc_y2 = []

with open('CurV 0gk 0.14V (10%) low and high pass flat stereo mode 1 Ohm.csv') as csvfile_1:
    pm = csv.reader(csvfile_1)
    for row in pm:
        x.append(float(row[3])*1000)
        curv10pc_y.append(float(row[4])*100)
        if (0.00025 < float(row[3])) and (float(row[3]) < 0.0047):
            x1.append(float(row[3])*1000)
        if (0.000018 < float(row[3])) and (float(row[3]) < 0.000033):
            x2.append(float(row[3])*1000)

csvfile_1.close()

with open('ResisV 0gk 0.14V (10%) low and high pass flat stereo mode 1 Ohm.csv') as csvfile_2:
    pm = csv.reader(csvfile_2)
    for row in pm:
        resv10pc_y.append(float(row[4])*10)
        if (0.00025 < float(row[3])) and (float(row[3]) < 0.0047):
            resv10pc_y1.append(float(row[4])*10)
        if (0.000018 < float(row[3])) and (float(row[3]) < 0.000033):
            resv10pc_y2.append(float(row[4])*10)

csvfile_2.close()

with open('PrimV 0gk 0.14V (10%) low and high pass flat stereo mode 1 Ohm.csv') as csvfile_3:
    pm = csv.reader(csvfile_3)
    for row in pm:
        priv10pc_y.append(float(row[4]))

csvfile_3.close()

fig, ax1 = plt.subplots()

plt.xlim(-0.5, 5.5)
ax2 = ax1.twinx()
ax3 = ax1.twinx()

ax1.set_xlabel('Time (ms)', fontsize=5)
ax1.set_ylabel('Primary voltage', color='tab:red', fontsize=5)
ax1.plot(x, priv10pc_y, color='tab:red', label='Pre-amplifier voltage')
ax1.tick_params(axis='y', labelcolor='tab:red', labelsize=5)

ax2.spines["right"].set_position(("axes", -0.1))
ax2.set_ylabel('Amplified voltage', color='tab:blue', labelpad=-25, fontsize=5)
ax2.plot(x, resv10pc_y, color='tab:blue', label='Post-amplifier')
ax2.tick_params(axis='y', labelcolor='tab:blue', labelsize=5)

ax3.spines["right"].set_position(("axes", -0.15))
ax3.set_ylabel('Current', color='tab:orange', labelpad=-25, fontsize=5)
ax3.plot(x, curv10pc_y, color='tab:orange', label='Current')
ax3.tick_params(axis='y', labelcolor='tab:orange', labelsize=5)

fig.legend(loc='lower center', fancybox=True, shadow=True, ncol=5, prop={'size': 5})

ax1.set_ylim(-0.3, 0.3)
ax2.set_ylim(-20, 20)
ax3.set_ylim(-15, 15)

fig.tight_layout()

slope, intercept, r_value, p_value, std_err = stats.linregress(x1, resv10pc_y1)
resv10pc_y11 = []
for i in range(len(x1)):
    resv10pc_y11.append(intercept + slope*x1[i])

ax2.plot(x1, resv10pc_y11, 'r', label='fitted line')
droop_slope = slope
droop_intercept = intercept

slope, intercept, r_value, p_value, std_err = stats.linregress(x2, resv10pc_y2)
resv10pc_y22 = []
for i in range(len(x2)):
    resv10pc_y22.append(intercept + slope*x2[i])

ax2.plot(x2, resv10pc_y22, 'r', label='fitted line')
rise_slope = slope
rise_intercept = intercept

A = np.array([[droop_slope, -1], [rise_slope, -1]])
b = np.array([- droop_intercept, - rise_intercept])
z = np.linalg.solve(A, b)
y_val = z[1]

npc_x = (0.9 * y_val - rise_intercept)/rise_slope
tpc_x = (0.1 * y_val - rise_intercept)/rise_slope
rise_time = npc_x - tpc_x
droop_y = 5 * droop_slope + droop_intercept
droop_time = 5.0 - z[0]
droop = (((y_val - droop_y)/y_val) * 100)/droop_time
slew_rate_100pc = y_val/z[0]

with open("Results_10% (1 ohm).txt", "w") as text_file:
    print("The 100% amplified voltage is " + str(y_val) + " volts. The 10% amplified voltage is " + str(0.1 * y_val) +
          " \nvolts. The delay time is " + str(tpc_x) + " ms. ", file=text_file)
    print("The 90% amplified voltage is " + str(0.9 * y_val) + " volts, and the rise time is " + str(rise_time) +
          " \nms. ", file=text_file)
    print("The droop is " + str(droop) + "%/ms. ", file=text_file)
    print("The slew rate is " + str(slew_rate_100pc) + " V/ms. ", file=text_file)

plt.show()
plt.savefig("V vs. t (10%, 1 ohm).pdf")