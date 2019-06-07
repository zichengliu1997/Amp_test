import csv
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

x = []
x1 = []
x2 = []
x3 = []
x4 = []
v_in = []
v_out = []
x_io = []
curv10pc_y = []
resv10pc_y = []
priv10pc_y = []
priv10pc_y1 = []
priv10pc_y2 = []
resv10pc_y1 = []
resv10pc_y2 = []

with open('CurV 0gk 0.88V (63%) low and high pass flat stereo mode 5 Ohms.csv') as csvfile_1:
    pm = csv.reader(csvfile_1)
    for row in pm:
        x.append(float(row[3])*1000)
        curv10pc_y.append(float(row[4])*100)

csvfile_1.close()

with open('ResisV 0gk 0.88V (63%) low and high pass flat stereo mode 5 Ohms.csv') as csvfile_2:
    pm = csv.reader(csvfile_2)
    for row in pm:
        resv10pc_y.append(float(row[4])*10)
        if (-0.00072 < float(row[3])) and (float(row[3]) < -0.00025):
            x3.append(float(row[3])*1000)
            resv10pc_y1.append(float(row[4])*10)
        if (-0.00018 < float(row[3])) and (float(row[3]) < 0.00025):
            x4.append(float(row[3])*1000)
            resv10pc_y2.append(float(row[4])*10)
        if (-0.000745 < float(row[3])) and (float(row[3]) < -0.0005):
            x_io.append(float(row[3])*1000)
            v_out.append(float(row[4]))

csvfile_2.close()

with open('PrimV 0gk 0.88V (63%) low and high pass flat stereo mode 5 Ohms.csv') as csvfile_3:
    pm = csv.reader(csvfile_3)
    for row in pm:
        priv10pc_y.append(float(row[4]))
        if (-0.00073 < float(row[3])) and (float(row[3]) < -0.00026):
            x1.append(float(row[3])*1000)
            priv10pc_y1.append(float(row[4]))
        if (-0.00022 < float(row[3])) and (float(row[3]) < 0.00022):
            x2.append(float(row[3])*1000)
            priv10pc_y2.append(float(row[4]))
        if (-0.000745 < float(row[3])) and (float(row[3]) < -0.0005):
            v_in.append(float(row[4]))

csvfile_3.close()

fig, ax1 = plt.subplots()

# plt.xlim(-0.5, 5.5)
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

# ax1.set_ylim(-3, 3)
# ax2.set_ylim(-70, 70)
# ax3.set_ylim(-70, 70)

fig.tight_layout()

slope, intercept, r_value, p_value, std_err = stats.linregress(x1, priv10pc_y1)
print("Slope of negative linear gain: " + str(slope) + ". ")
priv10pc_y11 = []
for i in range(len(x1)):
    priv10pc_y11.append(intercept + slope*x1[i])

# ax1.plot(x1, priv10pc_y11, 'r', label='fitted line')

slope, intercept, r_value, p_value, std_err = stats.linregress(x2, priv10pc_y2)
print("Slope of positive linear gain: " + str(slope) + ". ")
priv10pc_y22 = []
for i in range(len(x2)):
    priv10pc_y22.append(intercept + slope*x2[i])

# ax1.plot(x2, priv10pc_y22, 'r', label='fitted line')

slope, intercept, r_value, p_value, std_err = stats.linregress(x3, resv10pc_y1)
print("Slope of positive linear gain: " + str(slope) + ". ")
resv10pc_y11 = []
for i in range(len(x3)):
    resv10pc_y11.append(intercept + slope*x3[i])

ax2.plot(x3, resv10pc_y11, 'r', label='fitted line')

slope, intercept, r_value, p_value, std_err = stats.linregress(x4, resv10pc_y2)
print("Slope of positive linear gain: " + str(slope) + ". ")
resv10pc_y22 = []
for i in range(len(x4)):
    resv10pc_y22.append(intercept + slope * x4[i])

ax2.plot(x4, resv10pc_y22, 'r', label='fitted line')

plt.figure(2)
plt.plot(v_in, v_out)
plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])

plt.show()