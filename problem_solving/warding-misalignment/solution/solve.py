# solve script for detecting if two line segments collide
#!/usr/bin/env python3

from reader import *

paths = read_paths_from_file("./input.txt")

def cross(x1, y1, x2, y2):
    """
    The cross product a × b of vectors a = (x1 , y1 ) and b = (x2 , y2 ) is defined to be x1 y2 − x2 y1
    It tells us the direction to which b turns when it is placed directly after a.
    """
    return (x1 * y2) - (x2 * y1)


def vector(a, b):
    """Return vector b - a denoted ->ab"""
    return (b[0] - a[0], b[1] - a[1])


def point_location(p, s1, s2):
    """
    Returns the cross product of (p - s1) × (p - s2)
    * result > 0 => p is to the left of line s1->s2
    * result < 0 => p is to the right
    * result == 0 => colinear
    """
    v1 = vector(s1, p)
    v2 = vector(s2, p)
    return cross(*v1, *v2)


def on_segment(p, q, r):
    # Returns True if q lies on the segment pr
    return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
            min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))


def check_paths_collide(our_path, enemy_path):
    p1, p2 = our_path
    q1, q2 = enemy_path

    # Case 01: the line segments are on the same line and overlap each other
    # cross product all the points
    d1 = point_location(p1, q1, q2)
    d2 = point_location(p2, q1, q2)
    d3 = point_location(q1, p1, p2)
    d4 = point_location(q2, p1, p2)

    if (d1 == 0 and d2 == 0) or (d3 == 0 and d4 == 0):
        return (on_segment(q1, p1, q2) or
                on_segment(q1, p2, q2) or
                on_segment(p1, q1, p2) or
                on_segment(p1, q2, p2))

    # Case 02: the line segments have a common vertex
    # check manually: a = c, a = d, b = c, and b = d
    if p1 == q1 or p1 == q2 or p2 == q1 or p2 == q2:
        return True

    # Case 03: the line segments have an intersection point that is not a vertex
    # cross product with one vector and two other points, have to be in other sides
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True

    return False


def generate_flag_from_paths(paths, flag_prefix, flag_suffix):
    flag = flag_prefix
    # Iterate over pairs of consecutive paths (0-1, 2-3, 4-5, ...)
    for i in range(0, len(paths) - 1, 2):
        if check_paths_collide(paths[i], paths[i + 1]):
            flag += str((i + (i + 1)) % 10)
    flag += flag_suffix
    return flag


if __name__ == "__main__":
    # Example: flag format - 'ingeneer{fake_flag}'
    flag_prefix = "1ng3neer2k25{"
    flag_suffix = "}"

    # Generate flag by checking collisions
    flag = generate_flag_from_paths(paths, flag_prefix, flag_suffix)
    print("Flag: " + flag)

