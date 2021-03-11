from . import const
import numpy as np

def isFloat(value):
    """Checks if a string can be converted into a floating point value.

    Args:
	    value (str): test if this object can be converted into a float.

    Returns:
	    bool: true if 'value' can be converted into a float, false otherwise.
    """
  
    try:
	    float(value)
	    return True
    except ValueError:
    	return False

def add_data_directory(fileName):
    """Prepends the data directory to a given file name.

    Args:
        fileName (str): name of file.

    Returns:
        str: file with prepended data directory.
    """

    dataDirectory = const.DATA_DIRECTORY[-const.LENGTH_OF_DATA_DIR:]
    path = dataDirectory + fileName
    return path

def raw_to_processed(fileName):
    """Takes a raw data file name (according to definition in functions.py) and 
    finds the name of the equivalent processed data file.

    Args:
        fileName (str): name of raw data file.

    Returns:
        str: name of equivalent processed data file.
    """

    return fileName.replace(const.RAW_DATA_PREFIX, const.PROCESSED_DATA_PREFIX)

def processed_to_raw(fileName):
    """Takes a processed data file name (according to definition in 
    functions.py) and finds the name of the equivalent raw data file.

    Args:
        fileName (str): name of processed data file.

    Returns:
        str: name of equivalent raw data file.
    """
    
    return fileName.replace(const.PROCESSED_DATA_PREFIX, const.RAW_DATA_PREFIX)

def moving_average(data, window_size):
    """Calculates a moving average using the given parameters.

    Calculates this by convolving the data with a list of ones.

    Args:
        data (list): the data to be smoothed.
        window_size (int): how many terms to include in the moving average - 
            equivalently, the window size of the convolution.

    Returns:
        list: smoothed list
    """

    return np.convolve(data, np.ones(window_size), 'valid') / window_size