def read_paths_from_file(filename):
    """Reads paths from a file and returns them as a list of tuples"""
    paths = []
    with open(filename, 'r') as f:
        # Skipping the first line (which contains the number of paths pairs)
        f.readline()
        for line in f:
            points = tuple(map(int, line.split()))
            # Assumes input is formatted as "x1 y1 x2 y2"
            paths.append(((points[0], points[1]), (points[2], points[3])))
    return paths
