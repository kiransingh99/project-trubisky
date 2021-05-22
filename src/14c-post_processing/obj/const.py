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
TRACKER_BARE_MINIMUM = "name,health status,processed file" # bare minimum content of the tracker file (just the header)
TRACKER_BARE_MINIMUM_LENGTH = len(TRACKER_BARE_MINIMUM.split(","))

# for all data files
COLUMN_HEADERS = ["time", "acc (e_r)", "acc (e_theta)", "acc (e_phi)", 
                            "w (e_r)", "w (e_theta)", "w (e_phi)", 
                            "euler (alpha)", "euler (beta)", "euler (gamma)"]
COLOURS = ['', '#1f77b4', '#ff7f0e', '#26a02c', 
                '#d62728', '#9467bd', '#8c564b',
                '#e377c2', '#7f7f7f', '#bcbd22']
SENSOR_OFFSETS = [0, 0.001, -0.150, -0.013 ,
                        -0.012, 0.005, 0.013, 
                        0.000, 0.000, 0.000]

NUMBER_OF_COLUMNS = len(COLUMN_HEADERS) # number of columns in raw data csv files

assert len(COLOURS) == NUMBER_OF_COLUMNS, \
    "Fatal (const.py):There are {} listed column colours; there should be {}."\
        .format(len(COLOURS), NUMBER_OF_COLUMNS)
assert len(SENSOR_OFFSETS) == NUMBER_OF_COLUMNS, \
    "Fatal (const.py):There are {} listed sensor offsets; there should be {}."\
        .format(len(SENSOR_OFFSETS), NUMBER_OF_COLUMNS)

# for raw data files
RAW_DATA_PREFIX = "RAW-"
RAW_DATA_TITLE_FORMAT = RAW_DATA_PREFIX + "yyyy.mm.dd-hh.mm.ss"
RAW_DATA_FILE_TYPE = ".csv"

# for processed data files
PROCESSED_DATA_PREFIX = "PRO-"
PROCESSED_DATA_FILE_TYPE = ".csv"

# health check values
untested = 0
failed = 1
passedWithWarnings = 2
passed = 3