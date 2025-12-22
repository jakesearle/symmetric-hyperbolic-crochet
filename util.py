import math


def sin_deg(degs):
    return math.sin(degs * math.pi / 180)


def fraction_approx_of_divisors(x, s):
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
