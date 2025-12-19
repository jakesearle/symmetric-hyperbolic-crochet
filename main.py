import math
from math import pi
from math import sinh
from pathlib import Path

import util

# Height of a crochet row in cm
#
# This is the average height of one row of crochet stitches.
# This can be calculated by making:
#   Row 0: 11ch, turn
#   Row 1: 1sc in each ch (10), turn
#   Row 2-12: 10sc (10), turn
# Measure the middle 10 rows and divide by 10.
HEIGHT = 0.6

# Radius of the finished hyperbolic plane in cm
R = 1.0

# If the value "C(n) / C(n-1)" is unchanged after this many rows, stop.
TAIL_RATIO_LEN = 5
# Or, if you prefer, just set a fixed number of rows:
NUM_ROWS = -1

def C_builder(r, h):
    def C(n):
        """Calculate the circumference of a circle in the hyperbolic plane."""
        return 2 * pi * r * sinh(n * h / R)
    return C


def factor_denominator_approx(x, s):
    best = None  # (error, a, b)

    for b in divisors(s):
        a = round(x * b)
        err = abs(x - a / b)

        if best is None or err < best[0]:
            best = (err, a, b)

    return best[1], best[2]

def divisors(n):
    divs = set()
    for i in range(1, int(math.isqrt(n)) + 1):
        if n % i == 0:
            divs.add(i)
            divs.add(n // i)
    return sorted(divs)

def crochet_instructions(target, base, row_num):
    if target < base:
        raise ValueError("This script handles increases only")

    incs = target - base
    if incs == 0:
        return f"{base}sc"
    if incs == base:
        return f"{base}inc"
    if incs > base:
        raise ValueError("This script handles only increases less than double the stitches")

    remaining = target - (incs * 2)
    sc_between = remaining // incs

    # This is a weird edge case where there are technically no sc between increases, so we flip sc and inc
    if sc_between == 0:
        scs = remaining
        body = f"{scs}[sc, inc]"

        remaining_incs = target - (scs * 3)
        tail = remaining_incs // 2
        head = remaining_incs - tail
        parts = [inc(head), body, inc(tail)]
        return ", ".join(parts)

    sub_group_len = sc_between + 2 # Nsc, inc
    remainder = target - (sub_group_len * incs)

    parts = []
    # Main repeat block
    sc_part = "sc" if sc_between == 1 else f"{sc_between}sc"
    parts.append(f"{incs}[{sc_part}, inc]")

    # Extra stitches
    if remainder:
        if remainder == 1:
            parts.append("sc")
        elif row_num % 2:  # Odd row
            tail = remainder // 2
            head = remainder - tail
            parts = [sc(head)] + parts + [sc(tail)]
        else:
            parts.append(sc(remainder))

    return ", ".join(parts)

def sc(n):
    return "sc" if n == 1 else f"{n}sc"

def inc(n):
    return "inc" if n == 1 else f"{n}inc"

def save_instructions(r=R, h=HEIGHT, tail_len=None, num_rows=None):
    if (tail_len is None) == (num_rows is None):
        raise TypeError("Exactly one of 'tail_len' or 'num_rows' must be provided")

    end_type = f"asymptotic-{tail_len}" if tail_len is not None else f"n_rows-{num_rows}"
    path_str = f"out/height-{h:.2f}cm/radius-{r:.2f}/{end_type}.txt"
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w+') as f:
        table = table_str(r=R, h=HEIGHT, tail_len=tail_len, num_rows=num_rows)
        f.write(table)

def table_str(r=R, h=HEIGHT, tail_len=None, num_rows=None):
    if (tail_len is None) == (num_rows is None):
        raise TypeError("Exactly one of 'tail_len or 'num_rows' must be provided")
    if tail_len is not None:
        num_rows = 1000  # Arbitrary large number

    C = C_builder(r, h)

    grid = [
        ['Row', 'C(n)', 'C(n) / C(n-1)', 'Nearby fraction', 'Increase ratio', 'Pattern', 'Est. st.'],
        [1, f'{C(1):.2f}', '', '', '', '6sc in a magic ring', '(6)'],
    ]
    stitches_in_round = 6
    for n in range(2, num_rows + 1):
        cn_cn1 = C(n) / C(n - 1)
        numer, denom = factor_denominator_approx(cn_cn1, stitches_in_round)
        base_st = stitches_in_round
        target_st = stitches_in_round * numer // denom
        pattern = crochet_instructions(target_st, base_st, n)
        stitches_in_round = target_st

        f_str = f"{numer}/{denom}"
        ir_str = f'{numer} in {denom}st'
        grid.append([n, f'{C(n):.2f}', f'{cn_cn1:.2f}', f_str, ir_str, pattern, f'({stitches_in_round})'])

        if TAIL_RATIO_LEN:
            tail_ratios = [row[2] for row in grid[-TAIL_RATIO_LEN:]]
            if len(set(tail_ratios)) == 1:
                break
    st = util.grid_str(grid)
    return st

def main():
    if TAIL_RATIO_LEN and TAIL_RATIO_LEN > 0:
        save_instructions(r=R, h=HEIGHT, tail_len=TAIL_RATIO_LEN)
    elif NUM_ROWS and NUM_ROWS > 0:
        save_instructions(r=R, h=HEIGHT, num_rows=NUM_ROWS)


if __name__ == '__main__':
    main()
