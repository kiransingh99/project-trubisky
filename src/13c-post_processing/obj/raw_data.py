from . import functions
#from . import global_tracker
import os.path
import csv

class RawData:
    #handles everything to do with raw data files

    def __init__(self,
                    showWarnings = True,
                    rawDataDirectory="..\\..\\..\\data\\",
                    number_of_columns=7):

        currentPath = os.path.abspath(os.path.dirname(__file__))

        #set class constants
        self.__RAW_DATA_DIRECTORY = os.path.join(currentPath, rawDataDirectory)
        self.__NUMBER_OF_COLUMNS = 7
        self.__MAX_THROW_TIME = 30000
        self.__ACCELEROMETER_WARNING_THRESHOLD = 150 #accelerometer set to 16G
        self.__GYRO_WARNING_THRESHOLD = 1900 #gyro set to 2000dps
        
        #define class variables
        self.showWarnings = True
        self.__warningsRaised = False

        print("raw data initialised at", self.RAW_DATA_DIRECTORY, "\n")

    @property
    def RAW_DATA_DIRECTORY(self):
        return self.__RAW_DATA_DIRECTORY

    @property
    def NUMBER_OF_COLUMNS(self):
        return self.__NUMBER_OF_COLUMNS

    @property
    def MAX_THROW_TIME(self):
        return self.__MAX_THROW_TIME

    @property
    def ACCELEROMETER_WARNING_THRESHOLD(self):
        return self.__ACCELEROMETER_WARNING_THRESHOLD

    @property
    def GYRO_WARNING_THRESHOLD(self):
        return self.__GYRO_WARNING_THRESHOLD


    def check_health_all_files(self):
        #iterate through each file in the folder and call check_health_one_file
        
        files_total = 0
        files_passed = 0
        files_failed = []
        tests_failed = []

        for entry in os.listdir(self.RAW_DATA_DIRECTORY):
            filePath = os.path.join(self.RAW_DATA_DIRECTORY, entry)
            if entry.endswith(".csv"): 
                files_total += 1
                allTestsPassed, error = self.check_health_one_file(filePath)
                if allTestsPassed:
                    files_passed += 1
                else:
                    files_failed.append(filePath[len(self.RAW_DATA_DIRECTORY)-6:])
                    tests_failed.append(error)
        
        print("\n\nAll tests complete. {}/{} passed.".format(files_passed, 
                                                        files_total))
        if len(files_failed) != 0:
            print("The following files failed a test:")
            for i in range(0, len(files_failed)):
                print("  {} : {}\n".format(files_failed[i], error[i]))
        return(1)

    def check_health_one_file(self, filePath):
        #call other functions to check file health
        #if any tests return false then end checks and return False
        #only exception is if times can be corrected then return true, but make 
        #it clear that it should be checked
        
        fileName = filePath[len(self.RAW_DATA_DIRECTORY)-6:]

        with open(filePath) as f:
            csv_file = csv.reader(f, delimiter=',')
            print("Testing {}... ".format(fileName), end="")

            previousTime = 0

            for row in csv_file:
                try:
                    self.__check_columns(row, csv_file.line_num)
                    self.__check_values(row, csv_file.line_num)
                    previousTime = self.__check_times(row, previousTime)
                except AssertionError as e:
                    print("Test failed:")
                    print("  {}\n".format(e.args[0]))
                    return(0, e.args[0].split(":"))

        if self.__warningsRaised:
            print("\nAll tests passed\n") #adjust formatting if warnings have been raised
        else:
            print("All tests passed")

        return(1, None)


    def __check_columns(self, row, line_num):
        #check that each row has exactly 7 columns
        assert len(row) == self.NUMBER_OF_COLUMNS,\
                "Check columns: {} columns on line {}. Should be {}"\
                .format(len(row), line_num, self.NUMBER_OF_COLUMNS)
        return None

    def __check_values(self, row, line_num):
        #check the values are numeric and within an appropriate range
        for i, value_str in enumerate(row):
            assert functions.isFloat(value_str),\
                    "Check values: row {} has non-float value ({}) in column {}"\
                    .format(line_num, value_str, line_num)

            if self.showWarnings:
            
                value = float(value_str)

                if i == 0:
                    if int(value) > self.MAX_THROW_TIME: #if time gets near 30 milliseconds
                        print("\nWarning: Time of throw exceeds {} on line {} ( = {})"
                                .format(self.MAX_THROW_TIME, line_num, value),
                                end="")
                        self.__warningsRaised = True
                elif i <= 3:
                    if abs(value) > self.ACCELEROMETER_WARNING_THRESHOLD:
                        print("\nWarning: Acceleration exceeds {} on row {}, item {} ( = {})"
                                .format(self.ACCELEROMETER_WARNING_THRESHOLD, line_num, i, value),
                                end="")
                        self.__warningsRaised = True
                elif i <= 6:
                    if abs(value) > self.GYRO_WARNING_THRESHOLD:
                        print("\nWarning: Acceleration exceeds {} on row {}, item {} ( = {})"
                                .format(self.GYRO_WARNING_THRESHOLD, line_num, i, value),
                                end="")
                        self.__warningsRaised = True
        
        return None

    def __check_times(self, row, previousTime):
        #check that the times in the file only ever increase
        #if a time decreases, send it to be corrected - then go back 5 rows and 
        #check them again
        assert int(row[0]) > previousTime,\
                "Check times: row {} has time {} less than previous row ({})"\
                .format(row, row[0], previousTime)
        return int(row[0])

    def __add_file_to_global(self, file):
        #sends the names of the files to the GlobalFile class to get added
        pass

    def add_metrics_to_global(self, metric):
        #sends the relevant files and data to GlobalFile class to get added
        #metric is the name of the metric (string)
        #call populate_metric
        pass

    def __writeToTracker(self, file, metric, data):
        #iterate through all the raw files, and calculate metric, and then 
        #write it to global tracker file under the appropriate metric heading
        pass

    def isHealthy(self, file):
        #returns True if file is healthy
        pass