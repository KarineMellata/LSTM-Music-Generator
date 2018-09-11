import argparse
import csv
import os
import struct
import wave

parser = argparse.ArgumentParser(description="Convert csv to wav.")
parser.add_argument("csv", help="csv file")
parser.add_argument("data", type=int, help="zero-based index of data row")
parser.add_argument("-f", dest="freq", metavar="SAMPLING_RATE", type=int, default=44100, help="sampling rate")
parser.add_argument("-s", dest="size", metavar="SAMPLE_SIZE", type=int, default=2, help="sample size in bytes")
args = parser.parse_args()

if args.size == 1:
    typecode = "b"
elif args.size == 2:
    typecode = "h"
elif args.size == 4:
    typecode = "l"
else:
    print("Unsupported sample size!")
    quit()

name, ext = os.path.splitext(args.csv)

if ext == "tsv":
    delim = ","
else:
    delim = "\t"

data = []
n_levels = 2 ** (8 * args.size - 1) - 1

file = open(args.csv, "r")
reader = csv.reader(file, delimiter=delim)
header = next(reader)
for row in reader:
    x = float(row[args.data])
    x = int(x * n_levels)
    data.append(x)
file.close()

binwave = struct.pack(typecode * len(data), *data)

w = wave.Wave_write(name + ".wav")
w.setnchannels(1)
w.setsampwidth(args.size)
w.setframerate(args.freq)
w.writeframes(binwave)
w.close()