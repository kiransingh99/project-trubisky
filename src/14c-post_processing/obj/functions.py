from . import const

def isFloat(value):
    """Checks if a string can be converted into a floating point value.

    Args:
	    value (str): test if this object can be converted into a float

    Returns:
	    bool: true if 'value' can be converted into a float, false otherwise
    """
  
    try:
	    float(value)
	    return True
    except ValueError:
    	return False

def add_data_directory(fileName):
    """Prepends the data directory to a given file name.

    Args:
        fileName (str): name of file

    Returns:
        str: file with prepended data directory
    """

    dataDirectory = const.DATA_DIRECTORY[-const.LENGTH_OF_DATA_DIR:]
    path = dataDirectory + fileName
    return path

def raw_to_processed(fileName): # DOCSTRING
    return fileName.replace(const.RAW_DATA_PREFIX, const.PROCESSED_DATA_PREFIX)

def processed_to_raw(fileName): # DOCSTRING
    return fileName.replace(const.PROCESSED_DATA_PREFIX, const.RAW_DATA_PREFIX)