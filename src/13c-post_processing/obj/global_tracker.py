from . import const
import csv
import sys

class GlobalFile:
    # ADD DOCSTRING
    # handles everything to do with the global file
    def __init__(self, fullInitialisation = True):
        # ADD DOCSTRING

        # define class attributes
        self.__TRACKER_EXISTS = False
        self.__TRACKER_COUNT_ROWS = 0
        self.__TRACKER_COUNT_COLUMNS = 0

        if fullInitialisation:
            self.__check_tracker_full() # check tracker file exists and has header row

    def __del__(self):
        """Destructor for class.
        """

        #print("GlobalFile object destroyed")
        pass

    @property
    def TRACKER_EXISTS(self):
        """Getter for variable.

        Returns:
            bool: True if tracker file has been open since the initialisation of 
                this object
        """

        return self.__TRACKER_EXISTS

    @property
    def TRACKER_COUNT_ROWS(self):
        """Getter for variable.

        Returns:
            int: the number of rows in the global tracker file
        """

        return self.__TRACKER_COUNT_ROWS

    @property
    def TRACKER_COUNT_COLUMNS(self):
        """Getter for variable.

        Returns:
            int: the number of columns in the global tracker file
        """

        return self.__TRACKER_COUNT_COLUMNS

    def set_TRACKER_EXISTS(self, value):
        """Setter for variable of the same name.

        Returns:
            bool: the new value of the variable
        """

        self.__TRACKER_EXISTS = value
        return self.__TRACKER_EXISTS

    def set_TRACKER_COUNT_ROWS(self, value):
        """Setter for variable of the same name.

        Returns:
            int: the new value of the variable
        """

        self.__TRACKER_COUNT_ROWS = value
        return self.__TRACKER_COUNT_ROWS

    def set_TRACKER_COUNT_COLUMNS(self, value):
        """Setter for variable of the same name.

        Returns:
            int: the new value of the variable
        """

        self.__TRACKER_COUNT_COLUMNS = value
        return self.__TRACKER_COUNT_COLUMNS


    def is_file_recorded(self, fileName):
        # ADD DOCSTRING
        
        #check if given filename has been recorded in the tracker
        with open(const.TRACKER_FILEPATH) as f:
            tracker_file = csv.reader(f)
            
            for row in tracker_file:
                if row[0] == fileName:
                    return True
            return False

    def add_file(self, fileName, errorStatus=0):
        # ADD DOCSTRING

        #check if file is already listed. If it is, return false, if not, add
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
        # ADD DOCSTRING
        #add another column to global tracker by adding a title and appending a
        #comma to each line
        pass

    def change_error_status(self, fileName, errorStatus):
        # ADD DOCSTRING

        #find given file in the document and mark it as healthy if it is not
        #already. Return True if completed, return False if no change mad
        #write_to_file function
        self.write_to_file(fileName, 1, errorStatus)
        return 1
    
    def write_to_file(self, fileName, columnNumber, data):
        # ADD DOCSTRING

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

    def __check_tracker_full(self):
        """Checks that the global tracker file can be found and opened, and that 
        it has the correct header. Measures properties of tracker.

        Only use this function if significant processing will be done on the 
        tracker file. Otherwise, it is a waste of resources, and so the short 
        version is more appropriate.
        
        First, tries to open the tracker file. If unsuccessful, it kills the 
        script. If successful, it counts the number of rows and columns. If the 
        file is empty, it adds a header row. If the file is not empty, it checks 
        that the header row includes the right headings.
        """

        try:
            f = open(const.TRACKER_FILEPATH)
        except FileNotFoundError as e:
            print("\n\nFatal (global tracker file does not exist):", e)
            print("Code exited with status 1")
            sys.exit(1)
        else:
            # print("Found global tracker file", const.TRACKER_FILENAME)
            self.set_TRACKER_EXISTS(True)
            
            tracker_file = csv.reader(f)

            # count the number of rows in the tracker file
            self.set_TRACKER_COUNT_ROWS(sum(1 for row in tracker_file))

            # if no data in file, add the bare minimum header row
            if self.TRACKER_COUNT_ROWS == 0:
                print("Global tracker file has no header row.")
                
                f.close()
                
                f = open(const.TRACKER_FILEPATH, "w")
                f.write(const.TRACKER_BARE_MINIMUM)
                f.close()
                
                print("Header row added.")
                f = open(const.TRACKER_FILEPATH)
                tracker_file = csv.reader(f)

            f.seek(0) # return to start of file

            # output warning if bare minimum header is not in the first line of the file
            if const.TRACKER_BARE_MINIMUM not in f.readline():
                print("Warning: global tracker file does not have correct header.")

            # count the number of columns in the tracker file
            self.set_TRACKER_COUNT_COLUMNS(len(next(tracker_file)))
                
            f.close()

    def __check_tracker_short(self):
        """Checks that the global tracker file can be found and opened, and that 
        it has the correct header. Measures properties of tracker.

        Only use this function if no significant processing will be done on the 
        tracker file. Otherwise, it does not set up the file properly, and so 
        the long version is more appropriate.
        
        First, tries to open the tracker file. If unsuccessful, it kills the 
        script. If successful, if the file is empty, it adds a header row.
        """

        try:
            f = open(const.TRACKER_FILEPATH)
        except FileNotFoundError as e:
            print("\n\nFatal (global tracker file does not exist):", e)
            print("Code exited with status 1")
            sys.exit(1)
        else:
            # print("Found global tracker file", const.TRACKER_FILENAME)
            self.set_TRACKER_EXISTS(True)

            # if no data in file, add the bare minimum header row
            if self.TRACKER_COUNT_ROWS == 0:
                print("Global tracker file has no header row.")
                
                f.close()
                
                f = open(const.TRACKER_FILEPATH, "w")
                f.write(const.TRACKER_BARE_MINIMUM)
                f.close()
                
                print("Header row added.")
                f = open(const.TRACKER_FILEPATH)
                
            f.close()

    def __add_row(self, fileName):
        # ADD DOCSTRING

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
        # ADD DOCSTRING
        #add another column to global tracker
        #in docstring, make a note saying remember to populate the colum with data
        #increase tracker_count_columns by one
        pass
