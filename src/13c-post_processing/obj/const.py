import os.path

__currentPath = os.path.abspath(os.path.dirname(__file__))
__dataDirectory="..\\..\\..\\data\\"

DATA_DIRECTORY = os.path.join(__currentPath, __dataDirectory)

TRACKER_FILENAME = "globalTracker.csv"
TRACKER_FILEPATH = os.path.join(DATA_DIRECTORY, TRACKER_FILENAME)

DELIMITER = ","