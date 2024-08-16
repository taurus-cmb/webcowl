import os

apidir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.join(apidir, os.pardir)

class Config:
    # Whether to use a directory of dirfiles to read the data
    # If False, will create fake testing data on the fly, without reading.
    #   This allows testing without the pain of installing pygetdata
    FAKE_DATA = "WEBCOWL_FAKE_DATA" in os.environ
    # If using dirfiles, give the directory in which to find them
    DATA_PATH = os.environ.get("WEBCOWL_DATA_PATH", os.path.join(basedir, "fake_data"))
    BASE_DIR = basedir
