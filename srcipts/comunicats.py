import numpy as np

arr = np.linspace(0, 1, 20)
# print(arr)
asd = np.linspace(2, 10, 20)

a = '2;angle;-1'
if a.find(';angle;') > 0:
    print(True)
with open('readme.txt', 'w') as f:
    for i, j in zip(arr, asd):
        f.write(str(i) + ',' + str(j))
        f.write('\n')
