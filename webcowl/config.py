import os
from dotenv import load_dotenv

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)

# allow environment variable to specify environment file to load
load_dotenv(os.environ.get("WEBCOWL_ENV_FILE", ".env"))

class Config:
    # Whether to use a directory of dirfiles to read the data
    # If False, will create fake testing data on the fly, without reading.
    #   This allows testing without the pain of installing pygetdata
    FAKE_DATA = "WEBCOWL_FAKE_DATA" in os.environ
    # If using dirfiles, give the directory in which to find them
    BASE_DIR = basedir
    SECRET_KEY = os.environ.get("WEBCOWL_SECRET_KEY", "testing key: not secret")
    # TODO allow directory of different owl files that can be loaded
    OWL_FILE = os.environ.get("WEBCOWL_OWL_FILE", os.path.join(basedir, "examples", "owl_config.yml"))
    COW_ROOT_MESSAGE = os.environ.get("WEBCOWL_COW_ROOT_MESSAGE", "system.HKsystem")
    COW_COMMAND_PORT = os.environ.get("WEBCOWL_COW_COMMAND_PORT", ("127.0.0.1", 3006))
    COW_INFO_PORT = os.environ.get("WEBCOWL_OWL_FILE", ("127.0.0.1", 3007))
