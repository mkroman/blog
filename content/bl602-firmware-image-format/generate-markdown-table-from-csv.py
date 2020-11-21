import sys
import csv

sizes = {
    'uint16_t': 2,
    'uint8_t': 1,
    'uint8_tx4': 4,
    'uint8_tx2': 2
}

input = sys.argv[1]
offset = 0x4

with open(input) as f:
  reader = csv.reader(f)
  next(reader)

  for row in reader:
    type_size = sizes.get(row[0])
    name = row[1]
    comment = row[2]

    print('| 0x0{:<3x} | 0x0{:<9x} | {:20} | {:<49} |'.format(offset, type_size, name, comment))
    offset = offset + type_size
