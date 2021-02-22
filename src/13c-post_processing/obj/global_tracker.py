from . import const
import csv
import sys

class GlobalFile:
    """Main class for managing the global tracker file.

    Attributes:
        __TRACKER_EXISTS (bool): 'True' if the tracker has been found and opened 
            since the object was constructed
        __TRACKER_COUNT_ROWS (int): the number of rows in the tracker file
        __TRACKER_COUNT_COLUMNS (int): the number of columns in the tracker file

    Methods:
        __init__ : class constructor
        __del__ : class destructor
        TRACKER_EXISTS : property which returns the variable of the same name 
        TRACKER_COUNT_ROWS : property which returns the variable of the same 
            name
        TRACKER_COUNT_COLUMNS : property which returns the variable of the same 
            name
        set_TRACKER_EXISTS : setter for variable of the same name
        set_TRACKER_COUNT_ROWS : setter for variable of the same name
        set_TRACKER_COUNT_COLUMNS : setter for variable of the same name
        add_file : lists a raw data file in the global tracker
        add_metric : adds a new column to the global tracker file
        change_error_status : change the error status of an entry already logged
        is_file_recorded : checks if a given file has been recorded in the 
            tracker already
        write_to_file : overwrites a metric for an entry already listed in the 
            file
        __check_tracker_full : sets up the tracker fully - required for in-depth 
            processing
        __check_tracker_partial : partially sets uo the tracker - less 
            computationally expensive
        __add_row : adds a row to the bottom of the tracker
    """


    def __init__(self, fullInitialisation = True):
        """Constructor for class. sets the class parameters.

        Initialisation of class can be full, or partial. When in doubt, use 
        full, but be aware this iterates through every row of the file, and can 
        waste processing resources.

        Args:
            fullInitialisation (bool, optional): controls whether initialisation 
                is full or partial. Defaults to True.
        """

        # define class attributes
        self.__TRACKER_EXISTS = False
        self.__TRACKER_COUNT_ROWS = 0
        self.__TRACKER_COUNT_COLUMNS = 0

        if fullInitialisation:
            self.__check_tracker_full()
        else:
            self.__check_tracker_partial()

    def __del__(self):
        """Destructor for class.
        """

        #print("GlobalFile object destroyed")
        pass

    @property
    def TRACKER_EXISTS(self):
        """Getter for variable of the same name.

        Returns:
            bool: 'True' if tracker file has been open since the initialisation 
                of this object
        """

        return self.__TRACKER_EXISTS

    @property
    def TRACKER_COUNT_ROWS(self):
        """Getter for variable of the same name.

        Returns:
            int: the number of rows in the global tracker file
        """

        return self.__TRACKER_COUNT_ROWS

    @property
    def TRACKER_COUNT_COLUMNS(self):
        """Getter for variable of the same name.

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


    def add_file(self, fileName, errorStatus=0):
        """Adds a given file with an error code to the tracker file.

        Checks if the file has already been recorded. If not then the file gets 
        added. If it has already been recorded, the entry is updated.

        Args:
            fileName (str): name of file to be added to the tracker file
            errorStatus (int, optional): Error status associated with the file. 
                Defaults to 0.

        Returns:
            bool: 'True' if file has been added successfully. 'False' otherwise
        """

        if self.is_file_recorded(fileName):
            print("File has already been recorded, repeated entry not added: ", 
                    fileName)
            self.change_error_status(fileName, errorStatus)
        else:
            self.__add_row(fileName)
            self.write_to_file(fileName, 1, errorStatus)
        return True

    def add_metric(self, heading, operation):
        """Adds a column to the global tracker file and populates it with values 
        returned from the 'operation' function.

        Iterates through each line and saves the data in a list. For the header, 
        the name of the new heading gets appended, and for every other row, the 
        value of the metric gets appended. Then the data get written back to the 
        tracker file.

        Args:
            heading (str): name of heading of new column
            operation (method (str)): the method that calculates the metric for 
                the entry

        Returns:
            bool: 'True' to signify function completion
        """
        
        # add operation on each row

        with open(const.TRACKER_FILEPATH) as f: # read only
            tracker_file = csv.reader(f)
            
            # for tracking during loop
            fileData = []

            for row in tracker_file:

                # ignore blank rows
                if len(row) == 0:
                    continue

                # add new heading if on first line
                if tracker_file.line_num == 1:
                    fileData.append(list(row))
                    fileData[0].append(heading)
                else: # add data velue if on any other line
                    i = tracker_file.line_num-1
                    fileData.append(list(row))
                    fileData[i].append(operation(fileData[i][0]))

            with open(const.TRACKER_FILEPATH, "w", newline="") as f: # writeable
                tracker_file = csv.writer(f)
                tracker_file.writerows(fileData) # write amended data to tracker file

        return True

    def change_error_status(self, fileName, errorStatus):
        """Changes the error status of a given file in the tracker.

        Args:
            fileName (str): name of file whose entry is to be updated
            errorStatus (int): error status associated with the file

        Returns:
            int: indicates successful completion of method
        """

        self.write_to_file(fileName, 1, errorStatus)
        return 1
    
    def is_file_recorded(self, fileName):
        """Checks if a given file is recorded in the tracker file.

        Iterates through each row of the file and checks if any pf the file 
        names passed to this method matches any of the ones passed to this 
        method.

        Args:
            fileName (str): name of file to find in tracker file

        Returns:
            bool: 'True' if the file is listed, 'False' otherwise
        """
        
        with open(const.TRACKER_FILEPATH) as f:
            tracker_file = csv.reader(f)
            
            for row in tracker_file:
                if row[0] == fileName:
                    return True # stop looking when you find the correct file
            return False

    def write_to_file(self, fileName, columnNumber, data):
        """Overwrites a given cell in the tracker file with data passed to the 
        method.

        Locates the correct row in the file by finding the entry dictated by the 
        'fileName' parameter. The row is saved as a list, and the entry is 
        changed, before writing the list back to the file.

        Args:
            fileName (str): name of file whose entry is to be updated
            columnNumber (int): the column in the row to be overwritten
            data (any): data to write into file, gets cast into a string

        Returns:
            bool: signifies complete execution of method
        """

        with open(const.TRACKER_FILEPATH, "r") as f: # read only
            tracker_file = csv.reader(f)

            # for tracking during loop
            rowNumber = 0
            fileData = []
            
            for row in tracker_file:
                # ignore blank rows
                if len(row) == 0:
                    continue
                fileData.append(list(row))
                if fileData[rowNumber][0] != fileName:
                    rowNumber += 1 # count non-blank rows until match is found

            fileData[rowNumber][columnNumber] = data

        with open(const.TRACKER_FILEPATH, "w", newline="") as f: # writeable
            tracker_file = csv.writer(f)
            tracker_file.writerows(fileData) # write amended data to tracker file
        return True

    def __check_tracker_full(self):
        """Checks that the global tracker file can be found and opened, and that 
        it has the correct header. Measures properties of tracker.

        Only use this method if significant processing will be done on the 
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
            if const.TRACKER_BARE_MINIMUM not in f.read():
                print("Warning: global tracker file does not have correct header.")

            f.seek(0)

            # count the number of columns in the tracker file
            self.set_TRACKER_COUNT_COLUMNS(len(next(tracker_file)))
                
            f.close()

    def __check_tracker_partial(self):
        """Checks that the global tracker file can be found and opened, and that 
        it has the correct header. Measures properties of tracker.

        Only use this method if no significant processing will be done on the 
        tracker file. Otherwise, it does not set up the file properly, and so 
        the long version is more appropriate.
        
        First, tries to open the tracker file. If unsuccessful, it kills the 
        script. If successful, if the file is empty, it adds a header row. Then 
        counts the columns of the file.
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

            # if no data in file, add the bare minimum header row
            try:
                next(tracker_file)
            except:
                print("Global tracker file has no header row.")
                
                f.close()
                
                f = open(const.TRACKER_FILEPATH, "w")
                f.write(const.TRACKER_BARE_MINIMUM)
                f.close()
                
                print("Header row added.")
                f = open(const.TRACKER_FILEPATH)
                tracker_file = csv.reader(f)
                 
            f.seek(0)
            
            # count the number of columns in the tracker file
            self.set_TRACKER_COUNT_COLUMNS(len(next(tracker_file)))

            f.close()

    def __add_row(self, fileName):
        """Private function to add a single row to the bottom of the CSV file.

        Creates an empty list of the correct length, and sets the first 
        element to the file name. This gets appended to the file.

        Args:
            fileName (str): name of the file to be recorded

        Returns:
            int: to signify completion of function
        """

        dataToWrite = [""] * self.TRACKER_COUNT_COLUMNS # one item for each column in file
        dataToWrite[0] = fileName # first element of list is first column of file
        # append data to file
        with open(const.TRACKER_FILEPATH, "a") as f:
            f.write("\n")
            f.write(", ".join(dataToWrite))

        return 1
