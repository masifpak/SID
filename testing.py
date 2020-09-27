import csv
import glob
# Open the file in read mode

for filepath in glob.iglob('data/*.txt'):
    print(filepath)