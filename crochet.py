import math


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
        # Split if even numbered
        if min_lo_per_group % 2 == 0:
            los = min_lo_per_group // 2
            steps = [stitch_str(los, lo_f), stitch_str(1, hi_f), stitch_str(los, lo_f)]
            return stitch_group(n_subgroups, steps)
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
    if any('[' in step for step in steps):
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
