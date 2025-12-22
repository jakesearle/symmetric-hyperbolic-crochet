import math
from abc import abstractmethod, ABC
from pathlib import Path

import crochet
import grid
import util


class Shape(ABC):
    def __init__(self, stitch_height=None, tail_len=None, num_rows=None):
        if not stitch_height:
            raise TypeError("Stitch height must be provided and greater than 0")
        self.stitch_height = stitch_height

        if (tail_len is None) == (num_rows is None):
            raise TypeError("Exactly one of 'tail_len or 'num_rows' must be provided")
        if tail_len is not None:
            num_rows = 1000  # Arbitrary large number
        self.tail_len = tail_len
        self.num_rows = num_rows

        self.shape_name = None

    @abstractmethod
    def make_instructions(self):
        pass

    @staticmethod
    def save_instruction_file(table, path_str):
        path = Path(path_str)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w+') as f:
            t_string = grid.build_str(table)
            f.write(t_string)

    def generate_table(self, c_method):
        table = [
            ['Row', 'C(n)', 'C(n) / C(n-1)', 'Nearby fraction', 'Increase ratio', 'Pattern', 'Est. st.'],
            [1, f'{c_method(1):.2f}', '', '', '', '6sc in a magic ring', '(6)'],
        ]
        stitches_in_round = 6
        for n in range(2, self.num_rows + 1):
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

            if self.tail_len:
                tail_ratios = [row[2] for row in table[-self.tail_len:]]
                if len(set(tail_ratios)) == 1:
                    break
        return table

class Cone(Shape):
    def __init__(self, theta, stitch_height=None, tail_len=None, num_rows=None):
        Shape.__init__(self, stitch_height=stitch_height, tail_len=tail_len, num_rows=num_rows)
        self.shape_name = "cone"
        self.theta = theta

    def make_instructions(self):
        c_func = self.circumference_builder()
        table = self.generate_table(c_func)
        n_rows = len(table) - 1
        path_str = f"output/stitch-height-{self.stitch_height:.2f}cm/{self.shape_name}/theta-{self.theta}/rows-{n_rows}.txt"
        self.save_instruction_file(table, path_str)

    def circumference_builder(self):
        tip_h = self.stitch_height / util.sin_deg(self.theta)

        def func(n):
            """Calculate the circumference of a cone in a circle."""
            h_s = (n - 1) * self.stitch_height  # Stitched slope height
            r = (tip_h + h_s) * util.sin_deg(self.theta)

            return 2 * math.pi * r

        return func

class HyperbolicPlane(Shape):
    def __init__(self, radius, stitch_height=None, tail_len=None, num_rows=None):
        Shape.__init__(self, stitch_height=stitch_height, tail_len=tail_len, num_rows=num_rows)
        self.shape_name = "hyperbolic-plane"
        self.radius = radius

    def make_instructions(self):
        c_func = self.circumference_builder()
        table = self.generate_table(c_func)
        n_rows = len(table) - 1
        path_str = f"output/stitch-height-{self.stitch_height:.2f}cm/{self.shape_name}/radius-{self.radius}/rows-{n_rows}.txt"
        self.save_instruction_file(table, path_str)

    def circumference_builder(self):
        def func(n):
            """Calculate the circumference of a circle in the hyperbolic plane."""
            return 2 * math.pi * self.radius * math.sinh(n * self.stitch_height / self.radius)

        return func

