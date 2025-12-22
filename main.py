from math import pi
from math import sinh
from pathlib import Path

import crochet
import grid
import util
from util import sin_deg

# My yarn types and how tall they are
PINK_MEDIUM = 0.60
RED_STUDIO_CLASSIC = 0.65

# Height of a crochet row in cm
#
# This is the average height of one row of crochet stitches.
# This can be calculated by making:
#   Row 0: 11ch, turn
#   Row 1: 1sc in each ch (10), turn
#   Row 2-12: 10sc (10), turn
# Measure the middle 10 rows and divide by 10.
HEIGHT = RED_STUDIO_CLASSIC


def hyperbolic_c_builder(h):
    def func(n):
        """Calculate the circumference of a circle in the hyperbolic plane."""
        # Radius of the hyperbolic plane
        # For the sake of ratios, this doesn't matter (?)
        r = 3.5
        return 2 * pi * r * sinh(n * h / r)

    return func


def conical_c_builder(h, theta):
    tip_h = h / sin_deg(theta)

    def func(n):
        """Calculate the circumference of a cone in a circle."""
        h_s = (n - 1) * h  # Stitched slope height
        r = (tip_h + h_s) * sin_deg(theta)

        return 2 * pi * r

    return func


SHAPE_BUILDERS = {
    "symmetric-hyperbolic-plane": hyperbolic_c_builder,
    "cone": conical_c_builder,
}

def save_instructions(shape_name, c_method, h=HEIGHT, tail_len=None, num_rows=None):
    if (tail_len is None) == (num_rows is None):
        raise TypeError("Exactly one of 'tail_len' or 'num_rows' must be provided")

    table = generate_table(c_method, tail_len=tail_len, num_rows=num_rows)
    rows_generated = len(table) - 1
    path_str = f"output/{shape_name}/height-{h:.2f}cm/rows-{rows_generated}.txt"
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w+') as f:
        t_string = grid.build_str(table)
        f.write(t_string)


def generate_table(c_method, tail_len=None, num_rows=None):
    if (tail_len is None) == (num_rows is None):
        raise TypeError("Exactly one of 'tail_len or 'num_rows' must be provided")
    if tail_len is not None:
        num_rows = 1000  # Arbitrary large number

    table = [
        ['Row', 'C(n)', 'C(n) / C(n-1)', 'Nearby fraction', 'Increase ratio', 'Pattern', 'Est. st.'],
        [1, f'{c_method(1):.2f}', '', '', '', '6sc in a magic ring', '(6)'],
    ]
    stitches_in_round = 6
    for n in range(2, num_rows + 1):
        cn_cn1 = c_method(n) / c_method(n - 1)
        numer, denom = util.fraction_approx_of_divisors(cn_cn1, stitches_in_round)
        base_st = stitches_in_round
        target_st = stitches_in_round * numer // denom
        pattern = crochet.crochet_instructions(denom, numer)
        if denom != base_st:
            n_repeat = base_st // denom
            pattern = crochet.stitch_group(n_repeat, [pattern])
        stitches_in_round = target_st

        f_str = f"{numer}/{denom}"
        ir_str = f'{numer} in {denom}st'
        table.append([n, f'{c_method(n):.2f}', f'{cn_cn1:.2f}', f_str, ir_str, pattern, f'({stitches_in_round})'])

        if tail_len:
            tail_ratios = [row[2] for row in table[-tail_len:]]
            if len(set(tail_ratios)) == 1:
                break
    return table


def main():
    shape_name = "cone"
    c_method = SHAPE_BUILDERS[shape_name](HEIGHT, 60)
    save_instructions(shape_name, c_method, tail_len=5)


if __name__ == '__main__':
    main()
