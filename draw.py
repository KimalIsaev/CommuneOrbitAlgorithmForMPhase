import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import csv
import sys

def from_filename_to_list_of_lists(filename):
    with open(filename, 'r') as read_obj:
        csv_reader = csv.reader(read_obj, delimiter=' ')  
        list_of_csv = list(csv_reader)
        return list_of_csv

not_transposed = from_filename_to_list_of_lists(Path(sys.argv[1]))
print(not_transposed)
to_draw = list(map(lambda x:list(map(float, x)),
        zip(*not_transposed)))
print(to_draw)
percision = 1
if (len(sys.argv) == 4):
    percision = float(sys.argv[3])
x_values = list(percision*np.arange(0, len(to_draw[0]), 1))

for y_values in to_draw:
    plt.plot(x_values, y_values)
plt.savefig(Path(sys.argv[2]))
