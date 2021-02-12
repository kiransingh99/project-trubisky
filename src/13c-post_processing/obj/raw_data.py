#from . import global_tracker
import os.path
import csv

class RawData:
    #handles everything to do with raw data files

    def __init__(self,
                    rawDataDirectory="..\\..\\..\\data\\",
                    number_of_columns=7):

        currentPath = os.path.abspath(os.path.dirname(__file__))

        #set class constants
        self.__RAW_DATA_DIRECTORY = os.path.join(currentPath, rawDataDirectory)
        self.__NUMBER_OF_COLUMNS = 7

        print("raw data initialised at", self.RAW_DATA_DIRECTORY, "\n")

    @property
    def RAW_DATA_DIRECTORY(self):
        return self.__RAW_DATA_DIRECTORY

    @property
    def NUMBER_OF_COLUMNS(self):
        return self.__NUMBER_OF_COLUMNS

    def check_health_all_files(self):
        #iterate through each file in the folder and call check_health_one_file
        
        files_total = 0
        files_passed = 0
        files_failed = []
        tests_failed = []

        for filename in os.listdir(self.RAW_DATA_DIRECTORY):
            filePath = os.path.join(self.RAW_DATA_DIRECTORY, filename)
            if filename.endswith(".csv"): 
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

            previousTime = 0

            for row in csv_file:
                try:
                    self.__check_columns(row, csv_file.line_num)
                    previousTime = self.__check_times(row, previousTime)
                except AssertionError as e:
                    print("\nTest failed on {}".format(fileName))
                    print("  ", e.args[0])
                    return(0, e.args[0].split(":"))

        print("All tests passed")
        return(1, None)


    def __check_columns(self, row, line_num):
        #check that each row has exactly 7 columns
        assert len(row) == self.NUMBER_OF_COLUMNS,\
                            "Check columns: {} columns on line {}. Should be {}"\
                            .format(len(row), line_num, self.NUMBER_OF_COLUMNS)
        return None

    def __check_times(self, row, previousTime):
        #check that the times in the file only ever increase
        #if a time decreases, send it to be corrected - then go back 5 rows and 
        #check them again
        assert int(row[0]) > previousTime, "Check times: row {} has time {} less than previous row ({})".format(row, row[0], previousTime)

        return int(row[0])

    def __check_values(self, file, row):
        #check the values are numeric and within an appropriate range
        pass

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