from . import const
from . import functions
from . import global_tracker
import csv
import inspect
import matplotlib.pyplot as plt
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
        overWrite (bool): set as 'True' if data in the global tracker file 
            should be overwritten if it is incorrect, otherwise set as 'False'
        showWarnings (bool): should be 'True' if the user wants any warnings 
            from the test outputted to the terminal

        fileName (str): file name (without path) to raw data file to analyse

    Methods:
        __init__ : class constructor
        health : (property) groups the 'health' methods
        individual : (property) groups the 'individual' methods
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
        DATA_DIRECTORY : {property) returns the constant of the same names. 
            Takes its value from the const.py file
        NUMBER_OF_COLUMNS : {property) returns the constant of the same name. 
            Takes its value from the const.py file
        THROW_TIME_WARNING_THRESHOLD : {property) returns the constant of 
            the same name
        ACCELEROMETER_WARNING_THRESHOLD : {property) returns the constant of 
            the same name
        GYRO_WARNING_THRESHOLD : {property) returns the constant of the same 
            name
        check_all_files : iterates through all files in the folder and passes 
            each one through to 'check_one_file'
        check_one_file : runs each test on each row of the given raw data file
        __add_file_to_tracker : adds a given file and its health status to the 
            global tracker, after testing it and determining its health status
        __check_columns : asserts that the number of columns in each row is 
            correct
        __check_values : asserts that the values in the raw data file are usable 
        __check_times : asserts that the recorded time strictly increases 
        __is_in_tracker : determines if a given file has already been logged in 
            the global tracker
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
        self.__THROW_TIME_WARNING_THRESHOLD = 25000 
        self.__ACCELEROMETER_WARNING_THRESHOLD = 150 # accelerometer set to 16G
        self.__GYRO_WARNING_THRESHOLD = 1900 # gyro set to 2000dps
        
        # define class variables
        self.showWarnings = showWarnings
        self.overwrite = overwrite
        self.__warningsRaised = False

        print("Raw data initialised at", self.DATA_DIRECTORY, "\n")
        if self.overwrite == True:
            print("Overwrite is on")
        else:
            print("Overwrite is off")
        if self.showWarnings == True:
            print("Warrnings are on")
        else:
            print("Warnings are off")
        print("\n")

    def __del__(self):
        """Destructor for class.
        """

        print("RawData object destroyed")

    @property
    def DATA_DIRECTORY(self):
        """Getter for constant of the same name.

        Returns:
            str: the path to the directory that stores the data files
        """
        
        return const.DATA_DIRECTORY

    @property
    def NUMBER_OF_COLUMNS(self):
        """Getter for constant of the same name.

        Returns:
            int: expected number of columns in the raw data files
        """
        
        return const.NUMBER_OF_COLUMNS

    @property
    def THROW_TIME_WARNING_THRESHOLD(self):
        """Getter for constant of the same name.

        Returns:
            int: constant to store the threshold for throw time, that, if 
                exceeded, raises a warning
        """

        return self.__THROW_TIME_WARNING_THRESHOLD

    @property
    def ACCELEROMETER_WARNING_THRESHOLD(self):
        """Getter for constant of the same name.

        Returns:
            int: constant to store the threshold for acceleration across each 
                axis, that, if exceeded, raises a warning
        """
        
        return self.__ACCELEROMETER_WARNING_THRESHOLD

    @property
    def GYRO_WARNING_THRESHOLD(self):
        """Getter for constant of the same name.

        Returns:
            int: constant to store the threshold for angular velocity across 
                each axis, that, if exceeded, raises a warning
        """

        return self.__GYRO_WARNING_THRESHOLD


    def check_all_files(self):
        """Iterates through each file in the data directory and runs tests on 
        them.

        Goes through each file in the directory that stores all the raw data 
        files. For any raw data CSV files, tests are run, unless the file is 
        already recorded in the tracker file and 'overwrite is set False. This 
        method simply passes each file to the 'check_one_file' method. After 
        testing all the files, results are displayed.

        Returns:
            int: returns 1 if method completed successfully
        """

        # variables for keeping track during the loop
        files_total = 0 # total files tested
        files_passed = 0 # total files passed
        files_failed = [] # list of files that failed a test
        tests_failed = [] # the corresponding tests that the files failed on

        # iterate through each file in directory where data files are kept
        for entry in os.listdir(self.DATA_DIRECTORY):
            filePath = os.path.join(self.DATA_DIRECTORY, entry)
            fileName = filePath[const.PATH_LENGTH_TO_DATA_DIR:]
            
            # only check raw data files saved as a csv 
            if entry[len(const.RAW_DATA_PREFIX):] == const.RAW_DATA_PREFIX:
                 if entry.endswith(".csv"): # only check CSV files

                    # if overwrite is False, it doesn't matter if the file has already been recorded
                    if not self.overwrite:
                        if self.__is_in_tracker(fileName):
                            continue
                    
                    # therefor file is a valid raw data CSV file
                    files_total += 1
                    allTestsPassed, error = self.check_one_file(filePath)
                    
                    if allTestsPassed >= const.passedWithWarnings:
                        files_passed += 1
                    else:
                        # record file name and error
                        files_failed.append(fileName)
                        tests_failed.append("{} ({})".format(error[0], error[1].strip()))
            
        # output results
        print("\n\nAll tests complete. {}/{} files passed.".format(files_passed, 
                                                            files_total))
        if len(files_failed) != 0:
            print("The following files failed a test:")

            for i in range(0, len(files_failed)):
                print("  {} : {}\n".format(files_failed[i], tests_failed[i]))

        return 1

    def check_one_file(self, filePath):
        """Checks health of one file and adds it to the global tracker file. 
        Returns a tuple with the health status as the first element and failure 
        messages, if any, as the second.

        Runs the following tests on each row:
            - ensures the number of columns are correct
            - ensures the data in each cell is readable and in the correct form
            - checks the time of each measurement (each row) strictly increases
        Stops checking the file as soon as a test fails. Any warnings, or error 
        messages resulting from failed tests get outputted.

        Args:
            filePath (str): full absolute file path to the file to be checked

        Returns:
            int: health status, which summarises the results of the tests
            str: failure message if test failed, NoneType otherwise
        """

        # shorten file path
        fileName = filePath[const.PATH_LENGTH_TO_DATA_DIR:]

        try:
            with open(filePath) as f:
                csv_file = csv.reader(f)
                print("Testing {}... ".format(fileName), end="")

                healthStatus = const.untested
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
                    print("\nTest failed on line {}:".format(csv_file.line_num))
                    print("  {}\n".format(e.args[0]))
                    
                    healthStatus = const.failed
                    
                    return(const.untested, e.args[0].split(":"))

                else:
                    if self.__warningsRaised:
                        healthStatus = const.passedWithWarnings
                        # adjust output formatting if warnings have been raised
                        print("\nAll tests passed with healtstatus {}\n"
                                .format(healthStatus))
                        self.__warningsRaised = False
                    else:
                        healthStatus = const.passed
                        print("All tests passed with healthstatus", healthStatus)

                    return(healthStatus, None)

                finally:
                    # regardless of test outcome, list file in tracker before method returns
                    self.__add_file_to_tracker(fileName, healthStatus)
            
        except FileNotFoundError as e:
            print("Raw data file could not be found:", e)     


    def __add_file_to_tracker(self, fileName, healthStatus=const.untested):
        """Private method to add a given file to the global tracker file with 
        a given healthStatus.

        Creates an instance of the GlobalFile class and calls the relevant 
        method in there to update the health status, if the file has already 
        been recorded, or adds the file altogether if it has not been recorded.

        Args:
            fileName (str): raw data file to be added
            healthStatus (int): the health status to be written. Defaults to 
                const.untested.

        Returns:
            int: returns 1 if completed successfully
        """

        G = global_tracker.GlobalFile(fullInitialisation = False)

        if self.__is_in_tracker(fileName):
            return G.change_health_status(fileName, healthStatus)
        else:
            return G.add_file(fileName, healthStatus)

    def __check_columns(self, row):
        """Private method to check how many columns there are in a given row 
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
        """Private method to check that the values in each row are valid and 
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
            
            value = int(float(value_str))

            if i == 0: # time
                if value >= self.THROW_TIME_WARNING_THRESHOLD:
                    if self.showWarnings: # only print if showWarnings is 'True'
                        print("\nWarning: Time of throw exceeds {} ( = {})"
                                .format(self.THROW_TIME_WARNING_THRESHOLD, value),
                                end="")
                    self.__warningsRaised = True
            elif i <= 3: # acceleration on each axis
                if abs(value) >= self.ACCELEROMETER_WARNING_THRESHOLD:
                    if self.showWarnings:
                        print("\nWarning: Acceleration exceeds {} in column {} ( = {})"
                            .format(self.ACCELEROMETER_WARNING_THRESHOLD, i, value),
                            end="")
                    self.__warningsRaised = True
            elif i <= 6: # angular velocity on each axis
                if abs(value) >= self.GYRO_WARNING_THRESHOLD:
                    if self.showWarnings:
                        print("\nWarning: Acceleration exceeds {} in column {} ( = {})"
                            .format(self.GYRO_WARNING_THRESHOLD, i, value),
                            end="")
                    self.__warningsRaised = True
        
        return None

    def __check_times(self, line_num, row, previousTime):
        """Private method to check that the time strictly increases within 
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

    def __is_in_tracker(self, fileName):
        """Checks if a given raw data file has been logged in the global tracker 
        file.

        Creates an instance of the globalFile class and calls the equivalent 
        method in there, and returns the result.

        Args:
            fileName (str): raw data file to be checked

        Returns:
            int: returns 1 if the file has been recorded, and 0 if the file has 
                not been recorded, or if the tracker file cannot be found.
        """

        G = global_tracker.GlobalFile(fullInitialisation = False)
        if G.TRACKER_EXISTS:
            return G.is_file_recorded(fileName)
        return 0



class _SingleRawDataFile:
    """Handler for processing of individual raw data files.

    Attributes:
        fileName (str) : name of the file to calculate the metric for
        filePath (str) : file path to the file which will be operated on

    Methods:
        __init__ : constructor for class
        operations : {property) groups the methods that calculate 
            metrics for the global tracker
        file_path : (property) getter for the attribute of the same name
        set_file_name : setter for the attribute of the same name
        get_health_status : checks if a file has been marked as healthy in the 
            tracker
        graph_sensor_data : creates a graph of the raw sensor data over time
        graph_flight_path : DOCSTRING
    """

    def __init__(self, fileName):
        """[summary]

        Args:
            fileName ([type]): [description]
        """
        self.fileName = fileName

    @property
    def operations(self, fileName=""):
        """Creates instance of _MetricCalculator as an object of 
        _SingleRawDataFile.

        Creates an instance of the '_MetricCalculator' class as an object 
        called 'self.operations', where 'self' is the name of the instance of 
        '_SingleRawDataFile'.

        Args:
            fileName (str, optional): name of the file to operate on. None that 
                this must be passed to the operations sub-method at some point. 
                Defaults to "".

        Returns:
            _MetricCalculator object: instance of class
        """

        return _MetricCalculator(fileName)
    
    @property
    def file_path(self):
        """Getter for the attribute of the same name.

        Assigns the value first, by adding the full file path to 
        'self.fileName'.

        Returns:
            str: path to the raw data file
        """
        
        self.filePath = const.DATA_DIRECTORY + self.fileName[const.LENGTH_OF_DATA_DIR:]
        return self.filePath

    def set_file_name(self, value):
        """Setter for the attribute of the same name.

        Args:
            value (str): name of the file to calculate metric(s) for

        Returns:
            str: the new value of the attribute
        """

        self.fileName = value
        return self.fileName


    def get_health_status(self):
        """Checks if a file has been marked as healthy..

        Args:
            fileName (str): name of file to check

        Returns:
            int: Health status of a file
        """

        fileName = self.fileName

        G = global_tracker.GlobalFile(fullInitialisation = False)
        return G.get_health_status(fileName)

    def graph_sensor_data(self):
        """Creates a graph of the raw sensor data over time.

        First, checks the raw data file has passed its health checks. Then 
        stores the data in each of the columns in its own list, which is used 
        to generate a graph of all the values together.

        Returns:
            int: signifies successful completion of the method
        """
        
        healthStatus = self.get_health_status()
        filePath = self.file_path

        if healthStatus == -1: # not in file
            print("File not found")
            return 0
        elif healthStatus <= const.failed: # failed or untested
            print("File has not been marked as healthy")
            return 0
        else: # healthy
            with open(filePath) as f:
                raw_data = csv.reader(f)
                data = []

                # create blank list of lists to store data
                for i in range(0, const.NUMBER_OF_COLUMNS):
                    data.append([])

                for row in raw_data:
                    for i, entry in enumerate(row):
                        data[i].append(float(entry))

            time = data[0]

            # plot each dataset against time on the same axes
            for i in range(1, len(data)):
                plt.plot(time, data[i], label=const.COLUMN_HEADERS[i])

            plt.title("Raw Sensor Data against Time")
            plt.xlabel('Time (ms)')
            plt.ylabel('Sensor values')
            plt.legend()
            plt.show()

            return 1

    def graph_flight_path(self): #COMPLETE, DOCSTRING
        print("TO DO THIS FUNCTION STILL")

class _MetricCalculator:
    """Object that calculates all the metrics.

    Attributes:
        fileName (str) : name of the file to calculate the metric for
        filePath (str) : file path to the file which will be operated on

    Methods:
        __init__ : constructor for class
        file_path : (property) getter for the attribute of the same name
        set_file_name : setter for the attribute of the same name
        all : runs all methods in this class that calculate a metric
        total_time : metric calculator for the time of the throw recorded
    """

    def __init__(self, fileName):
        """Constructor for class. Sets class attribute.

        Args:
            fileName (str): the name of the file to calculate a metric for
        """
        
        self.fileName = fileName
        
    @property
    def file_path(self):
        """Getter for the attribute of the same name.

        Assigns the value first, by adding the full file path to 
        'self.fileName'.

        Returns:
            str: path to the raw data file
        """
        
        self.filePath = const.DATA_DIRECTORY + self.fileName[const.LENGTH_OF_DATA_DIR:]
        return self.filePath
        
    def set_file_name(self, value):
        """Setter for the attribute of the same name.

        Args:
            value (str): name of the file to calculate metric(s) for

        Returns:
            str: the new value of the attribute
        """

        self.fileName = value
        return self.fileName


    def all(self, fileName=None, heading=False): # DOCSTRING
        """Executes all the methods in this class, except for setup ones.
        """

        # get a list of the methods in this class
        attrs = (getattr(self, name) for name in dir(self))
        methods = filter(inspect.ismethod, attrs)

        # run the methods except the set up ones
        for method in methods:
            try:
                if method == self.__init__:
                    continue
                elif method == self.all:
                    continue
                elif method == self.file_path:
                    continue
                elif method == self.set_file_name:
                    continue
                return method(fileName, heading) # execute method if not one of the above
            except TypeError:
                # can't handle methods with required arguments
                print("Couldn't execute method:", method)

    def total_time(self, fileName = None, heading=False):
        """Calculates a metric (total time of recording for a given throw)

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, each file listed is found, and the 
        metric is calculated for it.

        Args:
            fileName (str): name of the file to calculate the metric for
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to actually calculate the value. Defaults to 
                False.

        Returns:
            int: value of metric
        """

        if heading:
            return "time of throw" # title of column in tracker file

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)
    
        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                # get to end of file
                for row in csv_file:
                    pass
                time = int(row[0])
                return time
        except:
            print("Couldn't open file: ", fileName)