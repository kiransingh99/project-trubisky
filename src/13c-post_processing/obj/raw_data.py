from . import const
from . import functions
from . import global_tracker
import csv
import os.path
import sys

class RawData:
    """Main class for handling the raw data files transmitted from the ball.

    The methods of this class is divided into two sections: 'health', which 
    handles everything to do with checking the 'health' of one or more raw data 
    files, and 'individual', which deals with just one file at a time, primarily 
    to process and display the data within it. The first three attributes are 
    relevant to the 'health' methods, and the last one is relevant to the 
    'individual' methods.

    Attributes:
        __NUMBER_OF_COLUMNS (int): constant to store the expected number of 
            columns in the raw data files. Takes its value from the const.py 
            file
        overWrite (bool): set as 'True' if data in the global tracker file 
            should be overwritten if it is incorrect, otherwise set as 'False'
        showWarnings (bool): should be 'True' if the user wants any warnings 
            from the test outputted to the terminal

        fileName (str): file name (without path) to raw data file to analyse

    Methods:
        __init__ : class constructor
        health : the property which groups the 'health' methods
        individual : the property which groups the 'individual' methods
    """

    def __init__(self, 
                    overwrite=True, showWarnings=True,
                    fileName=""):
        """Constructor for class, sets the class attributes based on the 
        parameters passed in.

        Args:
            overwrite (bool, optional): whether or not to overwrite data if it 
                has already been listed in the file. Defaults to True.
            showWarnings (bool, optional): whether or not to print warnings 
                from the tests to the terminal. Defaults to True.
            fileName (str): name of file for analysis and processing. Required 
                if using 'individual' methods.
        """
        
        # define class variables            
        self.__NUMBER_OF_COLUMNS = const.NUMBER_OF_COLUMNS
        self.overwrite = overwrite
        self.showWarnings = showWarnings

        self.fileName = fileName

    @property
    def health(self):
        """Creates instance of _RawDataHealthChecker as an object of RawData.
        
        Creates an instance of the '_RawDataHealthChecker' class as an object 
        called 'self.health', where 'self' is the name of the instance of 
        'RawData'. Parameters passeed to '_RawDataHealthChecker' are as set by 
        the 'RawData' class attributes.

        Returns:
            _RawDataHealthChecker object: instance of class
        """

        return _RawDataHealthChecker(showWarnings = self.showWarnings, 
                                        overwrite = self.overwrite)
    
    @property
    def individual(self): 
        """Creates instance of _SingleRawDataFile as an object of RawData.
        
        Creates an instance of the '_SingleRawDataFile' class as an object 
        called 'self.individual', where 'self' is the name of the instance of 
        'RawData'. Parameters passeed to '_SingleRawDataFile' are as set by the 
        'RawData' class attributes. Catches exception in case 'self.fileName' 
        does not link to a usable file.

        Returns:
            _SingleRawDataFile object: instance of class
        """

        return _SingleRawDataFile(self.fileName)

class _RawDataHealthChecker:
    """Collection of methods that assess the health of the CSV file passed to 
    it.

    This class will check that the raw data files in the data directory have 
    been formatted correctly, and there are no entries that cannot be 
    manipulated to get useful data output.

    Attributes:
        __NUMBER_OF_COLUMNS (int): constant to store the expected number of 
            columns in the raw data files. Takes its value from the const.py 
            file
        __THROW_TIME_WARNING_THRESHOLD (int): constant to store the threshold 
            for throw time, that, if exceeded, raises a warning
        __ACCELEROMETER_WARNING_THRESHOLD (int): constant to store the threshold 
            for acceleration across each axis, that, if exceeded, raises a 
            warning
        __GYRO_WARNING_THRESHOLD (int): constant to store the threshold for 
            angular velocity across each axis, that, if exceeded, raises a 
            warning
        __warningsRaised (bool): a flag that stores if a warning has been raised 
            for the raw data file currently being checked
        overWrite (bool): set as 'True' if data in the global tracker file 
            should be overwritten if it is incorrect, otherwise set as 'False'
        showWarnings (bool): should be 'True' if the user wants any warnings 
            from the test outputted to the terminal

    Methods:
        __init__ : class constructor
        __del__ : class destructor
        NUMBER_OF_COLUMNS : property which returns the constant of the same name
        THROW_TIME_WARNING_THRESHOLD : property which returns the constant of 
            the same name
        ACCELEROMETER_WARNING_THRESHOLD : property which returns the constant of 
            the same name
        GYRO_WARNING_THRESHOLD : property which returns the constant of the same 
            name
        check_all_files : iterates through all files in the folder and passes 
            each one through to 'check_one_file'
        check_one_file : runs each test on each row of the given raw data file
        is_in_tracker : determines if a given file has already been logged in 
            the global tracker
        __add_file_to_tracker : adds a given file and its error status to the 
            global tracker, after testing it and determining its error status
        __check_columns : asserts that the number of columns in each row is 
            correct
        __check_values : asserts that the values in the raw data file are usable 
        __check_times : asserts that the recorded time strictly increases 
    """

    def __init__(self, overwrite, showWarnings):
        """Constructor for class, defines constants and  class attributes.

        Args:
            overwrite (bool, optional): whether or not to overwrite data if it 
                has already been listed in the file.
            showWarnings (bool, optional): whether or not to print warnings 
                from the tests to the terminal.
        """

        # set class constants
        self.__NUMBER_OF_COLUMNS = const.NUMBER_OF_COLUMNS
        self.__THROW_TIME_WARNING_THRESHOLD = 25000 
        self.__ACCELEROMETER_WARNING_THRESHOLD = 150 # accelerometer set to 16G
        self.__GYRO_WARNING_THRESHOLD = 1900 # gyro set to 2000dps
        
        # define class variables
        self.showWarnings = showWarnings
        self.overwrite = overwrite
        self.__warningsRaised = False

        print("Raw data initialised at", const.DATA_DIRECTORY, "\n")

    def __del__(self):
        """Destructor for class.
        """

        print("RawData object destroyed")

    @property
    def NUMBER_OF_COLUMNS(self):
        """Getter for constant

        Returns:
            int: expected number of columns in the raw data files
        """
        
        return self.__NUMBER_OF_COLUMNS

    @property
    def THROW_TIME_WARNING_THRESHOLD(self):
        """Getter for constant

        Returns:
            int: constant to store the threshold for throw time, that, if 
            exceeded, raises a warning
        """

        return self.__THROW_TIME_WARNING_THRESHOLD

    @property
    def ACCELEROMETER_WARNING_THRESHOLD(self):
        """Getter for constant

        Returns:
            int: constant to store the threshold for acceleration across each 
            axis, that, if exceeded, raises a warning
        """
        
        return self.__ACCELEROMETER_WARNING_THRESHOLD

    @property
    def GYRO_WARNING_THRESHOLD(self):
        """Getter for constant

        Returns:
            int: constant to store the threshold for angular velocity across 
            each axis, that, if exceeded, raises a warning
        """

        return self.__GYRO_WARNING_THRESHOLD


    def check_all_files(self):
        """Iterates through each file in the data directory and runs tests on 
        them.

        Goes through each file in the directory that stores all the raw data 
        files. For any CSV file other than the global tracker file, tests are 
        run, unless the file is already recorded in the tracker file and 
        'overwrite is set False. This method simply passes each file to the 
        'check_one_file' method. After testing all the files, results are 
        displayed.

        Returns:
            int: returns 1 if function completed successfully
        """

        # variables for keeping track during the loop
        files_total = 0 # total files tested
        files_passed = 0 # total files passed
        files_failed = [] # list of files that failed a test
        tests_failed = [] # the corresponding tests that the files failed on

        # iterate through each file in directory where data files are kept
        for entry in os.listdir(const.DATA_DIRECTORY):
            filePath = os.path.join(const.DATA_DIRECTORY, entry)
            fileName = filePath[const.PATH_LENGTH_TO_DATA_DIR:]
            
            if entry.endswith(".csv"): # only check CSV files
                if entry == const.TRACKER_FILENAME: # ignore global tracker file
                    continue

                # if overwrite is False, it doesn't matter if the file has already been recorded
                if not self.overwrite:
                    if self.is_in_tracker(fileName):
                        continue
                
                # therefor file is a valid raw data CSV file
                files_total += 1
                allTestsPassed, error = self.check_one_file(filePath)
                
                if allTestsPassed:
                    files_passed += 1
                else:
                    # record file name and error
                    files_failed.append(fileName)
                    tests_failed.append(error)
        
        # output results
        print("\n\nAll tests complete. {}/{} files passed.".format(files_passed, 
                                                            files_total))
        if len(files_failed) != 0:
            print("The following files failed a test:")

            for i in range(0, len(files_failed)):
                print("  {} : {}\n".format(files_failed[i], error[i]))
        
        return 1

    def check_one_file(self, filePath):
        """Checks health of one file and adds it to the global tracker file. 
        Returns a tuple with 1 as the first element if all tests were passed, 
        and 0 otherwise.

        Runs the following tests on each row:
            - ensures the number of columns are correct
            - ensures the data in each cell is readable and in the correct form
            - checks the time of each measurement (each row) strictly increases
        Stops checking the file as soon as a test fails. Any warnings, or error 
        messages resulting from failed tests get outputted.

        Args:
            filePath (str): full absolute file path to the file to be checked

        Returns:
            int: 1 if all tests passed, 0 otherwise
            str: error message if test failed, NoneType otherwise
        """

        # shorten file path
        fileName = filePath[const.PATH_LENGTH_TO_DATA_DIR:]

        with open(filePath) as f:
            csv_file = csv.reader(f)
            print("Testing {}... ".format(fileName), end="")

            errorStatus = 0 # errorStatus 0 means untested
            previousTime = 0 # to ensure time on each row always increases

            try:
                # run tests on each row
                for row in csv_file:
                    self.__check_columns(row)
                    self.__check_values(row)
                    previousTime = self.__check_times(csv_file.line_num, 
                                                        row,
                                                        previousTime)
                
            except AssertionError as e: # test failed
                print("Test failed on line {}:".format(csv_file.line_num))
                print("  {}\n".format(e.args[0]))
                
                errorStatus = 1 # errorStatus 1 means tested but failed
                
                return(0, e.args[0].split(":"))

            else:
                if self.__warningsRaised:
                    # adjust output formatting if warnings have been raised
                    print("\nAll tests passed\n")
                    self.__warningsRaised = False
                    errorStatus = 2 # errorStatus 2 means passed with warnings
                else:
                    print("All tests passed")
                    errorStatus = 3 # errorStatus 3 means passed without warnings

                return(1, None)

            finally:
                # regardless of test outcome, list file in tracker before function returns
                self.__add_file_to_tracker(fileName, errorStatus)

    def is_in_tracker(self, fileName):
        """Checks if a given raw data file has been logged in the global tracker 
        file.

        Creates an instance of the globalFile class and calls the equivalent 
        function in there, and returns the result.

        Args:
            fileName (str): raw data file to be checked

        Returns:
            int: returns 1 if the file has been recorded, and 0 if the file has 
            not been recorded, or if the tracker file cannot be found.
        """

        G = global_tracker.GlobalFile()
        if G.TRACKER_EXISTS:
            return G.is_file_recorded(fileName)
        return 0

    def __add_file_to_tracker(self, fileName, errorStatus=0):
        """Private function to add a given file to the global tracker file with 
        a given errorStatus.

        Creates an instance of the GlobalFile class and calls the relevant 
        function in there to update the error status, if the file has already 
        been recorded, or adds the file altogether if it has not been recorded.

        Args:
            fileName (str): raw data file to be added
            errorStatus (int): the error status to be written. Defaults to 0.

        Returns:
            int: returns 1 if completed successfully, 0 otherwise
        """

        G = global_tracker.GlobalFile()
        if G.TRACKER_EXISTS:
            if self.is_in_tracker(fileName):
                return G.change_error_status(fileName, errorStatus)
            else:
                return G.add_file(fileName, errorStatus)
        else:
            print("Could not find tracker file")
        return 0

    def __check_columns(self, row):
        """Private function to check how many columns there are in a given row 
        object of a CSV file.

        Receives the row from the CSV handler and asserts that the length of it 
        is the expected value, as defined in the class constants.

        Args:
            row (list): row object from the CSV file

        Returns:
            NoneType: signifies completion, and no assertion error
        """

        assert len(row) == self.NUMBER_OF_COLUMNS,\
                "Check columns: {} columns - should be {}"\
                .format(len(row), self.NUMBER_OF_COLUMNS)
        return None

    def __check_values(self, row):
        """Private function to check that the values in each row are valid and 
        usable.

        Receives the row object from the CSV handler and first checks if it has 
        numerical data in it. Then, depending on the column, and therefore the 
        type of data, checks to see if it is within an acceptable range, and if 
        not, raises a warning.

        Args:
            row (list): row object from the CSV file

        Returns:
            NoneType: signifies completion, and no assertion error
        """

        # iterate through each element in the row
        for i, value_str in enumerate(row):

            # check the element has data, and that it can be cast into a float
            assert len(value_str.strip()) > 0,\
                    "Check values: no data in column {}".format(i)
            assert functions.isFloat(value_str),\
                    "Check values: non-float value ({}) in column {}"\
                    .format(value_str, i)

            # the rest of the function just raises warnings, skip if not needed
            if self.showWarnings:
            
                value = float(value_str)

                if i == 0: # time
                    if int(value) > self.THROW_TIME_WARNING_THRESHOLD:
                        print("\nWarning: Time of throw exceeds {} ( = {})"
                                .format(self.THROW_TIME_WARNING_THRESHOLD, value),
                                end="")
                        self.__warningsRaised = True
                elif i <= 3: # acceleration on each axis
                    if abs(value) > self.ACCELEROMETER_WARNING_THRESHOLD:
                        print("\nWarning: Acceleration exceeds {} in column {} ( = {})"
                                .format(self.ACCELEROMETER_WARNING_THRESHOLD, i, value),
                                end="")
                        self.__warningsRaised = True
                elif i <= 6: # angular velocity on each axis
                    if abs(value) > self.GYRO_WARNING_THRESHOLD:
                        print("\nWarning: Acceleration exceeds {} in column {} ( = {})"
                                .format(self.GYRO_WARNING_THRESHOLD, i, value),
                                end="")
                        self.__warningsRaised = True
        
        return None

    def __check_times(self, line_num, row, previousTime):
        """Private function to check that the time strictly increases within 
        the raw data file.

        Receives the row object from the CSV handler and first asserts that the 
        time has not decreased since the last reading. Then it assertts that the 
        time has not remained constant either.

        Args:
            row (list): row object from the CSV file
            previousTime (int): the time recorded on the previous row

        Returns:
            int: time recorded on this row
        """

        assert int(row[0]) >= previousTime,\
                "Check times: row {} has time less than previous row ({} -> {})"\
                .format(line_num, row[0], previousTime)
        assert int(row[0]) > previousTime,\
                "Check times: row {} has time equal to previous row ({})"\
                .format(line_num, row[0])
        return int(row[0])



class _SingleRawDataFile:
    def __init__(self, fileName):
        # test if filename can be opened and raise error if not
        
        filePath = os.path.join(const.DATA_DIRECTORY, fileName)
        
        try:
            f = open(filePath)
        except FileNotFoundError as e:
            print("\n\nFatal (raw data file does not exist):", e)
            print("Code exited with status 1")
            sys.exit(1)
        else:
            # do stuff
                
            f.close()

    
    def __add_file_to_tracker(self, fileName):
        # sends the names of the files to the GlobalFile class to get added
        errorStatus = 0
        G = global_tracker.GlobalFile()
        G.add_file(fileName, errorStatus)
        del G

    def add_metrics_to_tracker(self, metric):
        # sends the relevant files and data to GlobalFile class to get added
        # metric is the name of the metric (string)
        # call populate_metric
        pass

    def __write_to_tracker(self, file, metric, data):
        # iterate through all the raw files, and calculate metric, and then 
        # write it to global tracker file under the appropriate metric heading
        pass

    def isHealthy(self, file):
        # returns True if file is healthy
        pass
