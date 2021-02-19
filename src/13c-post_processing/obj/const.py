import os.path

# private constants used to set up public ones
__currentPath = os.path.abspath(os.path.dirname(__file__))
__dataDirectory="..\\..\\..\\data\\"

# absolute path to directory where data files are stored
DATA_DIRECTORY = os.path.join(__currentPath, __dataDirectory)
PATH_LENGTH_TO_DATA_DIR = len(DATA_DIRECTORY)-6

# for the global tracker file
TRACKER_FILENAME = "globalTracker.csv"
TRACKER_FILEPATH = os.path.join(DATA_DIRECTORY, TRACKER_FILENAME) # full file path

DELIMITER = "," # used in csv files
NUMBER_OF_COLUMNS = 7 # number of columns in raw data csv files