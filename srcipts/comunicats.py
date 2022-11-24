import os
x_angle_global = [1, 2, 3]
y_angle_global = [2, 4, 5]
# folder path
import os

dir_path = r'../data'
count = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
