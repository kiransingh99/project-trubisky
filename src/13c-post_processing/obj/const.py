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
TRACKER_BARE_MINIMUM = "name,error status" # bare minimum content of the tracker file (just the header)

# for raw data files
NUMBER_OF_COLUMNS = 7 # number of columns in raw data csv files