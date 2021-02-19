from . import functions
from . import global_tracker
from . import const
import os.path
import csv

class RawData:
    #handles everything to do with raw data files
    def __init__(self, 
                    showWarnings=True, overwrite=False,
                    fileName=""):
        
        #define class variables            
        self.showWarnings = showWarnings
        self.overwrite = overwrite
        self.number_of_columns = 7

        self.fileName = fileName

    @property
    def health(self):
        return _RawDataHealthChecker(showWarnings = self.showWarnings, 
                                        overwrite = self.overwrite,
                                        number_of_columns = self.number_of_columns)
    
    @property
    def individual(self):
        return _SingleRawDataFile(self.fileName)


class _RawDataHealthChecker:
    def __init__(self, showWarnings, overwrite, number_of_columns):
        
        #set class constants
        self.__NUMBER_OF_COLUMNS = number_of_columns
        self.__THROW_TIME_WARNING_THRESHOLD = 25000 
        self.__ACCELEROMETER_WARNING_THRESHOLD = 150 #accelerometer set to 16G
        self.__GYRO_WARNING_THRESHOLD = 1900 #gyro set to 2000dps
        
        #define class variables
        self.showWarnings = showWarnings
        self.__warningsRaised = False
        self.overwrite = overwrite

        print("Raw data initialised at", const.DATA_DIRECTORY, "\n")

    def __del__(self):
        print("RawData object destroyed")

    @property
    def NUMBER_OF_COLUMNS(self):
        return self.__NUMBER_OF_COLUMNS

    @property
    def THROW_TIME_WARNING_THRESHOLD(self):
        return self.__THROW_TIME_WARNING_THRESHOLD

    @property
    def ACCELEROMETER_WARNING_THRESHOLD(self):
        return self.__ACCELEROMETER_WARNING_THRESHOLD

    @property
    def GYRO_WARNING_THRESHOLD(self):
        return self.__GYRO_WARNING_THRESHOLD


    def check_all_files(self):
        #iterate through each file in the folder and call check_health_one_file
        
        files_total = 0
        files_passed = 0
        files_failed = []
        tests_failed = []

        for entry in os.listdir(const.DATA_DIRECTORY):
            filePath = os.path.join(const.DATA_DIRECTORY, entry)
            if entry.endswith(".csv"): 
                if entry == const.TRACKER_FILENAME:
                    continue
                if not self.overwrite:
                    fileName = filePath[len(const.DATA_DIRECTORY)-6:]
                    if self.is_in_tracker(fileName):
                        continue
                files_total += 1
                allTestsPassed, error = self.check_one_file(filePath)
                if allTestsPassed:
                    files_passed += 1
                else:
                    files_failed.append(filePath[len(const.DATA_DIRECTORY)-6:])
                    tests_failed.append(error)
        
        print("\n\nAll tests complete. {}/{} files passed.".format(files_passed, 
                                                            files_total))
        if len(files_failed) != 0:
            print("The following files failed a test:")

            for i in range(0, len(files_failed)):
                print("  {} : {}\n".format(files_failed[i], error[i]))
        
        return 1

    def check_one_file(self, filePath):
        #call other functions to check file health
        #if any tests return false then end checks and return False
        #only exception is if times can be corrected then return true, but make 
        #it clear that it should be checked
        
        fileName = filePath[len(const.DATA_DIRECTORY)-6:]

        with open(filePath) as f:
            csv_file = csv.reader(f)
            print("Testing {}... ".format(fileName), end="")

            errorStatus = 0
            previousTime = 0

            try:
                for row in csv_file:
                    self.__check_columns(row)
                    self.__check_values(row)
                    previousTime = self.__check_times(csv_file.line_num, row, previousTime)
                
            except AssertionError as e:
                print("Test failed on line {}:".format(csv_file.line_num))
                print("  {}\n".format(e.args[0]))
                errorStatus = 1
                return(0, e.args[0].split(":"))

            else:
                if self.__warningsRaised:
                    print("\nAll tests passed\n") #adjust formatting if warnings have been raised
                    self.__warningsRaised = False
                    errorStatus = 2
                else:
                    print("All tests passed")
                    errorStatus = 3

                return(1, None)

            finally:
                self.__add_file_to_tracker(fileName, errorStatus)
                    
    def __check_columns(self, row):
        #check that each row has exactly 7 columns
        assert len(row) == self.NUMBER_OF_COLUMNS,\
                "Check columns: {} columns - should be {}"\
                .format(len(row), self.NUMBER_OF_COLUMNS)
        return None

    def __check_values(self, row):
        #check the values are numeric and within an appropriate range
        for i, value_str in enumerate(row):
            assert len(value_str.strip()) > 0,\
                    "Check values: no data in column {}".format(i)
            assert functions.isFloat(value_str),\
                    "Check values: non-float value ({}) in column {}"\
                    .format(value_str, i)

            if self.showWarnings:
            
                value = float(value_str)

                if i == 0:
                    if int(value) > self.THROW_TIME_WARNING_THRESHOLD: #if time gets near 30 milliseconds
                        print("\nWarning: Time of throw exceeds {} ( = {})"
                                .format(self.THROW_TIME_WARNING_THRESHOLD, value),
                                end="")
                        self.__warningsRaised = True
                elif i <= 3:
                    if abs(value) > self.ACCELEROMETER_WARNING_THRESHOLD:
                        print("\nWarning: Acceleration exceeds {} in column {} ( = {})"
                                .format(self.ACCELEROMETER_WARNING_THRESHOLD, i, value),
                                end="")
                        self.__warningsRaised = True
                elif i <= 6:
                    if abs(value) > self.GYRO_WARNING_THRESHOLD:
                        print("\nWarning: Acceleration exceeds {} in column {} ( = {})"
                                .format(self.GYRO_WARNING_THRESHOLD, i, value),
                                end="")
                        self.__warningsRaised = True
        
        return None

    def __check_times(self, line_num, row, previousTime):
        #check that the times in the file only ever increase
        #if a time decreases, send it to be corrected - then go back 5 rows and 
        #check them again
        assert int(row[0]) > previousTime,\
                "Check times: row {} has time less than previous row ({} -> {})"\
                .format(line_num, row[0], previousTime)
        return int(row[0])

    def __add_file_to_tracker(self, fileName, errorStatus):
        #sends the names of the files to the GlobalFile class to get added
        G = global_tracker.GlobalFile()
        if G.TRACKER_EXISTS:
            if self.is_in_tracker(fileName):
                return G.change_error_status(fileName, errorStatus)
            else:
                return G.add_file(fileName, errorStatus)
        else:
            print("Could not find tracker file")
        return 0

    def is_in_tracker(self, fileName):
        #returns True if object is already being tracked
        G = global_tracker.GlobalFile()
        if G.TRACKER_EXISTS:
            return G.is_file_recorded(fileName)
        return 0

class _SingleRawDataFile:
    def __init__(self, fileName):
        #test if filename can be opened and catch error if not
        pass

    
    def __add_file_to_tracker(self, fileName):
        #sends the names of the files to the GlobalFile class to get added
        errorStatus = 0
        G = global_tracker.GlobalFile()
        G.add_file(fileName, errorStatus)
        del G

    def add_metrics_to_tracker(self, metric):
        #sends the relevant files and data to GlobalFile class to get added
        #metric is the name of the metric (string)
        #call populate_metric
        pass

    def __write_to_tracker(self, file, metric, data):
        #iterate through all the raw files, and calculate metric, and then 
        #write it to global tracker file under the appropriate metric heading
        pass

    def isHealthy(self, file):
        #returns True if file is healthy
        pass
