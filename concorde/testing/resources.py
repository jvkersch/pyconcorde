from importlib_resources import files


def get_dataset_path(fname):
    return files("concorde.testing.data").joinpath(fname)
