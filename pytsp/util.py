ADMISSIBLE_NORMS = {
    "EUC_2D"
}


def write_tsp_file(fp, xs, ys, norm, name):
    """ Write data to a TSPLIB file.
    """
    if len(xs) != len(ys):
        raise ValueError(
            "x and y coordinate vector must have the "
            "same length ({} != {})".format(len(xs), len(ys))
        )
    if norm not in ADMISSIBLE_NORMS:
        raise ValueError(
            "Norm {!r} must be one of {}"
            .format(norm, ', '.join(ADMISSIBLE_NORMS))
        )

    fp.write("NAME: {}\n".format(name))
    fp.write("TYPE: TSP\n")
    fp.write("DIMENSION: {}\n".format(len(xs)))
    fp.write("EDGE_WEIGHT_TYPE: {}\n".format(norm))
    fp.write("NODE_COORD_SECTION\n")
    for n, (x, y) in enumerate(zip(xs, ys), start=1):
        fp.write("{} {} {}\n".format(n, x, y))
    fp.write("EOF\n")
