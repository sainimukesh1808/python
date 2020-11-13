import csv

output = []

row = []
with open("D:\Target_Data.csv", newline="") as f:
    data = csv.reader(f)
    for line in data:
        row.append(line)
print(row)
# for line in f:
#     cells = line.split( "," )
#     output.append( ( cells[ 17 ] ) )
#
# print(output)
# f.close()
# Test.append(output[7:37])
