from . import const
import csv
import sys

class GlobalFile:
    #handles everything to do with the global file
    def __init__(self):

        try:
            f = open(const.TRACKER_FILEPATH)
        except FileNotFoundError as e:
            print("\n\nFatal (global tracker file does not exist):", e)
            print("Code exited with status 1")
            sys.exit(1)
        else:
            #print("Found global tracker file", const.TRACKER_FILENAME)
            self.__TRACKER_EXISTS = True
            
            tracker_file = csv.reader(f)

            self.set_TRACKER_COUNT_ROWS(sum(1 for row in tracker_file))

            if self.TRACKER_COUNT_ROWS == 0:
                print("Global tracker file has no header row.")
                
                f.close()
                
                f = open(const.TRACKER_FILEPATH, "w")
                f.write(const.TRACKER_BARE_MINIMUM)
                f.close()
                
                print("Header row added.")
                f = open(const.TRACKER_FILEPATH)
                tracker_file = csv.reader(f)
            
            f.seek(0)
            self.set_TRACKER_COUNT_COLUMNS(len(next(tracker_file)))
                
            f.close()

    def __del__(self):
        #print("GlobalFile object destroyed")
        pass

    @property
    def TRACKER_EXISTS(self):
        return self.__TRACKER_EXISTS

    @property
    def TRACKER_COUNT_ROWS(self):
        return self.__TRACKER_COUNT_ROWS

    @property
    def TRACKER_COUNT_COLUMNS(self):
        return self.__TRACKER_COUNT_COLUMNS


    def set_TRACKER_COUNT_ROWS(self, value):
        self.__TRACKER_COUNT_ROWS = value
        return self.__TRACKER_COUNT_ROWS

    def set_TRACKER_COUNT_COLUMNS(self, value):
        self.__TRACKER_COUNT_COLUMNS = value
        return self.__TRACKER_COUNT_COLUMNS


    def add_file(self, fileName, errorStatus=0):
        #check if file is already listed. If it is, return false, if not, aadd
        #metrics from untracked files to global tracker file and mark health
        #as 'False' (and return True)
        if self.is_file_recorded(fileName):
            print("File has already been recorded, repeated entry not added.")
            return False
        else:
            self.__add_row(fileName)
            self.write_to_file(fileName, 1, errorStatus)
            return True

    def add_metric(self, heading, fileName):
        #add another column to global tracker by adding a title and appending a
        #comma to each line
        pass

    def __add_row(self, fileName):
        #add another row to global tracker - might be easier to open it as a 
        #normal file and add a row equal to the filename followed by a bunch of commas
        #in docstring, make a note saying remember to populate the row with data
        #increase tracker_count_rows by one
        dataToWrite = [""] * self.TRACKER_COUNT_COLUMNS
        dataToWrite[0] = fileName
        with open(const.TRACKER_FILEPATH, "a") as f:
            f.write("\n")
            f.write(", ".join(dataToWrite))

    def __add_column(self, file):
        #add another column to global tracker
        #in docstring, make a note saying remember to populate the colum with data
        #increase tracker_count_columns by one
        pass

    def change_error_status(self, fileName, errorStatus):
        #find given file in the document and mark it as healthy if it is not
        #already. Return True if completed, return False if no change mad
        #write_to_file function
        self.write_to_file(fileName, 1, errorStatus)
        return 1
    
    def write_to_file(self, fileName, columnNumber, data):
        #write given data to tracker file, with the row and column given by
        #'file' and 'metric' respectively
        with open(const.TRACKER_FILEPATH, "r") as f:
            tracker_file_r = csv.reader(f)
            rowNumber = 0
            fileData = []
            for row in tracker_file_r:
                if len(row) == 0:
                    continue
                fileData.append(list(row))
                if fileData[rowNumber][0] != fileName:
                    rowNumber += 1
            fileData[rowNumber][columnNumber] = data
        with open(const.TRACKER_FILEPATH, "w", newline="") as f:
            tracker_file_w = csv.writer(f)
            tracker_file_w.writerows(fileData)
        return True

    def is_file_recorded(self, fileName):
        #check if given filename has been recorded in the tracker
        with open(const.TRACKER_FILEPATH) as f:
            tracker_file = csv.reader(f)
            next(tracker_file) # skip header
            for row in tracker_file:
                if row[0] == fileName:
                    return True
            return False
