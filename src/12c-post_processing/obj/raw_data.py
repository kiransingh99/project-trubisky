import global_tracker

class RawData:
    #handles everything to do with raw data files

    def __init__(self):

        print("raw data initialised")

    def check_health(self, file):
        #call other functions to check file health
        #if any tests return false then end checks and return False
        #only exception is if times can be corrected then return true, but make 
        #it clear that it should be checked
        pass

    def __check_columns(self, file):
        #check that each row has exactly 7 columns
        pass

    def __check_times(self, file):
        #check that the times in the file only ever increase
        #if a time decreases, send it to be corrected - then go back 5 rows and 
        #check them again
        pass

    def __correct_times(self, file, row):
        #if any times are wrong, attempt to correct them by replacing the time
        #with the average of the times before and after
        pass

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