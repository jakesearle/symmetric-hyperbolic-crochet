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
R = 3.5

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


def crochet_instructions(base, target):
    if target < base:
        raise ValueError("This script handles increases only")

    ratio = target / base
    hi_f, lo_f = math.ceil(ratio), math.floor(ratio)
    if hi_f == lo_f:
        return stitch_str(base, ratio)

    min_stitches = lo_f * base
    n_hi = target - min_stitches
    n_subgroups = n_hi
    n_lo = base - n_hi
    min_lo_per_group = n_lo // n_subgroups
    extra_los = n_lo % n_subgroups
    if extra_los == 0:
        steps = [stitch_str(min_lo_per_group, lo_f), stitch_str(1, hi_f)]
        return stitch_group(n_subgroups, steps)
    if extra_los == 1:
        main_steps = [stitch_str(min_lo_per_group, lo_f), stitch_str(1, hi_f)]
        main_str = stitch_group(n_subgroups, main_steps)
        steps = [main_str, stitch_str(1, lo_f)]
        return stitch_group(1, steps)

    normal_subgroups = n_subgroups - extra_los
    ext_subgroups = extra_los
    norm_steps = [stitch_str(min_lo_per_group, lo_f), stitch_str(1, hi_f), ]
    norm_str = stitch_group(normal_subgroups, norm_steps)
    extended_steps = [stitch_str(min_lo_per_group + 1, lo_f), stitch_str(1, hi_f)]
    ext_str = stitch_group(ext_subgroups, extended_steps)
    return stitch_group(1, [norm_str, ext_str])


def stitch_group(n_repeat, steps):
    steps = [s for s in steps if s]
    if len(steps) == 1:
        step = steps[0]
        if n_repeat == 1:
            return step
        if step.isalpha():
            return f'{n_repeat}{step}'

    steps_str = ", ".join(steps)
    if n_repeat == 1:
        return steps_str
    padding = ''
    if any(['[' in step for step in steps]):
        padding = ' '
    return f'{n_repeat}[{padding}{steps_str}{padding}]'


def stitch_str(n_repeat, n_factor):
    if n_repeat < 0 or n_factor < 0:
        raise ValueError("Positive values only")

    if n_factor == 1:
        stitch_desc = "sc"
    elif n_factor == 2:
        stitch_desc = "inc"
    else:
        stitch_desc = f"{n_factor:.0f}sc in 1"

    if n_repeat == 0:
        return ''
    elif n_repeat == 1:
        return stitch_desc
    if n_repeat > 1 and n_factor <= 2:
        return f"{n_repeat}{stitch_desc}"
    return f"{n_repeat}[{stitch_desc}]"


def save_instructions(r=R, h=HEIGHT, tail_len=None, num_rows=None):
    if (tail_len is None) == (num_rows is None):
        raise TypeError("Exactly one of 'tail_len' or 'num_rows' must be provided")

    end_type = f"asymptotic-{tail_len}" if tail_len is not None else f"n_rows-{num_rows}"
    path_str = f"output/height-{h:.2f}cm/radius-{r:.2f}/{end_type}.txt"
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
        pattern = crochet_instructions(denom, numer)
        if denom != base_st:
            n_repeat = base_st // denom
            pattern = stitch_group(n_repeat, [pattern])
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


def test():
    base = 11
    for target in range(base, base * 3 + 1):
        # if target not in [13, 16, 17, 21]:
        #     continue
        i = crochet_instructions(base, target)
        print(f'({base}->{target}): {i}')


def generate_default_files():
    rs = [1, 3, 3.5, 4.0, 5.0, 9.0]
    for r in rs:
        save_instructions(r=r, h=HEIGHT, tail_len=TAIL_RATIO_LEN)


def generate_one_off():
    if TAIL_RATIO_LEN and TAIL_RATIO_LEN > 0:
        save_instructions(r=R, h=HEIGHT, tail_len=TAIL_RATIO_LEN)
    elif NUM_ROWS and NUM_ROWS > 0:
        save_instructions(r=R, h=HEIGHT, num_rows=NUM_ROWS)


def main():
    generate_default_files()


if __name__ == '__main__':
    main()
