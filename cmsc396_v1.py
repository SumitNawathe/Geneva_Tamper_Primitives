import io

# tcp
input = """
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Source Port          |       Destination Port        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sequence Number                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Acknowledgment Number                      |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Data |           |U|A|P|R|S|F|                               |
   | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
   |       |           |G|K|H|T|N|N|                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Checksum            |         Urgent Pointer        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Options                    |    Padding    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                             data                              |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""
# udp
# input = """
#                   0      7 8     15 16    23 24    31
#                  +--------+--------+--------+--------+
#                  |     Source      |   Destination   |
#                  |      Port       |      Port       |
#                  +--------+--------+--------+--------+
#                  |                 |                 |
#                  |     Length      |    Checksum     |
#                  +--------+--------+--------+--------+
#                  |
#                  |          data octets ...
#                  +---------------- ...
# """
# ip
# input = """
#     0                   1                   2                   3
#     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |Version|  IHL  |Type of Service|          Total Length         |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |         Identification        |Flags|      Fragment Offset    |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |  Time to Live |    Protocol   |         Header Checksum       |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                       Source Address                          |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                    Destination Address                        |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                    Options                    |    Padding    |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# """
input = input.split('\n')

# remove empty lines
input = list(filter(lambda l: len(l) > 0, input))

# remove beginning whitespace
beg_wspace_amt = min(len(line) - len(line.lstrip()) for line in input if len(line) > 0)
input = list(map(lambda l: str(l[beg_wspace_amt:]), input))
print('\n'.join(input))  # log

# find divider line
line = None
for line in input:
    if len(set(line.strip())) <= 2: break
if line is None:
    exit(1) # failure
divide_chars = {'-', '|', '+'}
print(f"{divide_chars=}")

# convert to 2D array of characters
char_arr = list(map(lambda l: list(l.strip()), input))
i = input.index(line)  # index of first divider line
n, m = len(char_arr), len(char_arr[0])
print(f"{i=}")

lst = []

while i+1 < n:
    i += 1
    starti = i
    while i < n and not set(input[i].strip()).issubset(divide_chars):
        i += 1
    endi = i
    if starti == endi or endi >= n: continue

    j = 0
    while j+1 < m:
        j += 1
        startj = j
        while input[starti][j] not in divide_chars:
            j += 1
        endj = j

        s = ""
        for x in range(starti, endi):
            for y in range(startj, endj):
                s += char_arr[x][y]
        lst.append((' '.join(s.strip().split()), starti, endi, startj, endj))

print(lst)


# group into rows
rows = []
curr_row = []
prevj = -1
for t in lst:
    if t[3] < prevj:
        rows.append(curr_row)
        curr_row = []
    curr_row.append(t)
    prevj = t[4]
if len(curr_row) > 0:
    rows.append(curr_row)

print(rows)


# harcode: how many bits is a row
bits_per_row = 32

ans = []
for row in rows:
    s = sum(t[4]-t[3]+1 for t in row)
    for x in row:
        ans.append((x[0], int(bits_per_row*(x[4]-x[3]+1)/s)))

print(ans)


# generate python code


