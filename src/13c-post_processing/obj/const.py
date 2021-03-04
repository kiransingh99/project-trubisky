import os.path

# private constants used to set up public ones
__currentPath = os.path.abspath(os.path.dirname(__file__))
__dataDirectory = "\\data\\"
__relativeToDataDirectory = "..\\..\\.." + __dataDirectory

# path to directory where data files are stored
DATA_DIRECTORY = os.path.join(__currentPath, __relativeToDataDirectory) # full absolute path
LENGTH_OF_DATA_DIR = len(__dataDirectory)
PATH_LENGTH_TO_DATA_DIR = len(DATA_DIRECTORY)-LENGTH_OF_DATA_DIR # relative to project folder

# for the global tracker file
TRACKER_FILENAME = "globalTracker.csv"
TRACKER_FILEPATH = os.path.join(DATA_DIRECTORY, TRACKER_FILENAME) # full file path
TRACKER_BARE_MINIMUM = "name,health status" # bare minimum content of the tracker file (just the header)
TRACKER_BARE_MINIMUM_LENGTH = len(TRACKER_BARE_MINIMUM.split(","))

# for raw data files
NUMBER_OF_COLUMNS = 7 # number of columns in raw data csv files
COLUMN_HEADERS = ["time", "acc_x", "acc_y", "acc_z", "w_x", "w_y", "w_z"]
COLOURS = ['','#1f77b4', '#ff7f0e', '#26a02c', '#d62728', '#9467bd', '#8c564b']

assert len(COLUMN_HEADERS) == NUMBER_OF_COLUMNS, \
    "Fatal (const.py):There are {} listed column headers; there should be {}."\
        .format(len(COLUMN_HEADERS), NUMBER_OF_COLUMNS)
assert len(COLOURS) == NUMBER_OF_COLUMNS, \
    "Fatal (const.py):There are {} listed column colours; there should be {}."\
        .format(len(COLOURS), NUMBER_OF_COLUMNS)

RAW_DATA_PREFIX = "RAW-"
RAW_DATA_TITLE_FORMAT = RAW_DATA_PREFIX + "yyyy.mm.dd-hh.mm.ss"
RAW_DATA_FILE_TYPE = ".csv"

# for health check values
untested = 0
failed = 1
passedWithWarnings = 2
passed = 3