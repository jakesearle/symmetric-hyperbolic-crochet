import model

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
STITCH_HEIGHT = RED_STUDIO_CLASSIC


def make_standard_instructions():
    # Cones
    angles = [10, 17, 30, 45, 60]
    for a in angles:
        model.Cone(a, stitch_height=STITCH_HEIGHT, num_rows=15).make_instructions()

    # Hyperbolic Planes
    radii = [1.0, 3.0, 3.5, 4.0, 9.0]
    for r in radii:
        model.HyperbolicPlane(r, stitch_height=STITCH_HEIGHT, tail_len=5).make_instructions()

def main():
    make_standard_instructions()


if __name__ == '__main__':
    main()
