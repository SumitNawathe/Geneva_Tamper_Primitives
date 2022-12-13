import io
from typing import List, Tuple

def parse_diagram(input: str, bits_per_row: int = 32, logging: bool = False) -> List[Tuple[str, int]]:
    # split into lines
    input = input.split('\n')

    # remove empty lines
    input = list(filter(lambda l: len(l) > 0, input))

    # remove beginning whitespace
    beg_wspace_amt = min(len(line) - len(line.lstrip()) for line in input if len(line) > 0)
    input = list(map(lambda l: str(l[beg_wspace_amt:]), input))
    if logging: print('\n'.join(input))

    # find divider line
    line = None
    for line in input:
        if len(set(line.strip())) <= 2: break
    if line is None:
        exit(1) # failure
    divide_chars = {'-', '|', '+'}
    if logging: print(f"{divide_chars=}")

    # convert to 2D array of characters
    char_arr = list(map(lambda l: list(l.strip()), input))
    i = input.index(line)  # index of first divider line
    n, m = len(char_arr), len(char_arr[0])
    if logging: print(f"{i=}")

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
    if logging: print(lst)


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
    if logging: print(rows)

    ans = []
    for row in rows:
        s = sum(t[4]-t[3]+1 for t in row)
        for x in row:
            ans.append((x[0], int(bits_per_row*(x[4]-x[3]+1)/s)))
    if logging: print(ans)

    # remove "data"/"payload" from end (not part of header)
    if ans[-1][0].lower() in ['data', 'payload']:
        ans.pop(-1)

    return ans


def collect_options(lst: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    output = []
    curr_flags = []
    num_flag_sections = 0
    for (name, size) in lst:
        if size == 1:
            curr_flags.append(name)
        else:
            if len(curr_flags) == 0:
                output.append((name, size))
            else:
                if len(curr_flags) == 1: output.append((curr_flags[0], 1))
                else:output.append((f"Flags{'' if num_flag_sections == 0 else num_flag_sections}", len(curr_flags)))
                curr_flags = []
                num_flag_sections += 1
    if len(curr_flags) != 0:
        if len(curr_flags) == 1: output.append((curr_flags[0], 1))
        else: output.append((f"Flags{'' if len(curr_flags) == 0 else len(curr_flags)}", len(curr_flags)))
    return output


def make_abbr(lst: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    output = []
    for (name, size) in lst:
        split = name.split(' ')
        if split[-1].lower() == 'Number':
            split[-1] = 'Num'
        elif split[-1].lower() == 'Address':
            split[-1] = 'Addr'
        output.append(('_'.join(map(lambda w: w.lower(), split)), size))
    return output
