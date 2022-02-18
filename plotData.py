import numpy as np
import matplotlib.pyplot as plt
import json

data = np.genfromtxt('data/Simulation/Simulation_2022_02_18__17_08_41/events.dat',
                     skip_header=1,
                     skip_footer=0,
                     names=True,
                     dtype=None,
                     delimiter='\t')

print(data)
i=0
G1=[]
G2=[]
G3=[]
while i < len(data):
    try:
        G1+=[json.loads(data[i][4])[0]]
        G2+=[json.loads(data[i][4])[1]]
        G3+=[json.loads(data[i][4])[2]]
    except:
        if i == 0:
            G1+=[0]
            G2+=[0]
            G3+=[0]
        else:
            G1+=[G1[i-1]]
            G2+=[G2[i-1]]
            G3+=[G3[i-1]]
    i+=1

T=[float(t[0]) for idx, t in enumerate(data)]

fig, ax = plt.subplots()
ax.plot(T, G1, 'r', label='red')
ax.plot(T, G2, 'g', label='green')
ax.plot(T, G3, 'b', label='blue')
ax.legend()
plt.ylabel('Goal sigmoided activation')
plt.xlabel('Time [s]')
plt.show()