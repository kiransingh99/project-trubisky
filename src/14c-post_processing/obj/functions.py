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
    path = dataDirectory + fileName.split("\\")[-1]
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
        data (list[float]): the data to be smoothed.
        window_size (int): how many terms to include in the moving average - 
            equivalently, the window size of the convolution.

    Returns:
        list: smoothed list
    """

    return np.convolve(data, np.ones(window_size), 'valid') / window_size

def generate_dcm(yaw, pitch, roll):
    """Generates a direction cosine matrix based on the values of the Euler 
    angles provided as parameters.

    Precalculates each trigonometric function, for efficiency. Then calculates 
    each element of the matrix by products of the functions.

    Args:
        yaw (float): yaw angle in Euler set.
        pitch (flaot): pitch angle in Euler set.
        roll (float): roll angle in Euler set.

    Returns:
        list[[float]]: direction cosine matrix.
    """

    sin_y = np.sin(yaw)
    cos_y = np.cos(yaw)
    sin_p = np.sin(pitch)
    cos_p = np.cos(pitch)
    sin_r = np.sin(roll)
    cos_r = np.cos(roll)

    dcm = np.zeros((3,3))
    dcm[0,0] = cos_y*cos_p
    dcm[0,1] = cos_y*sin_p*sin_r - sin_y*cos_r
    dcm[0,2] = cos_y*sin_p*cos_r + sin_y*sin_r
    dcm[1,0] = sin_y*cos_p
    dcm[1,1] = sin_y*sin_p*sin_r + cos_y*cos_r
    dcm[1,2] = sin_y*sin_p*cos_r - cos_y*sin_r
    dcm[2,0] = -sin_p
    dcm[2,1] = cos_p*sin_r
    dcm[2,2] = cos_p*cos_r

    return dcm
