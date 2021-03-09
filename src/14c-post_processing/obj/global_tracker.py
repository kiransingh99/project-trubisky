from . import const
from . import raw_data
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
        TRACKER_EXISTS : (property) getter for the attribute of the same name
        TRACKER_COUNT_ROWS : (property) getter for the attribute of the same  
            name
        TRACKER_COUNT_COLUMNS : (property) getter for the attribute of the same  
            name
        set_TRACKER_EXISTS : setter for attribute of the same name
        set_TRACKER_COUNT_ROWS : setter for attribute of the same name
        set_TRACKER_COUNT_COLUMNS : setter for attribute of the same name
        add_file : lists a raw data file in the global tracker
        add_metric : adds a new column to the global tracker file
        get_column_number : returns the column number of a given heading
        populate_metric : populates/ updates an existing column in the global 
            tracker file
        remove_deleted : removes a file from the tracker if the file has been 
            deleted
        remove_metric : removes a column from the tracker file
        change_health_status : change the health status of an entry already 
            logged
        get_health_status : checks if a file is marked as healthy in the global tracker
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

        # print("GlobalFile object destroyed")
        pass

    @property
    def TRACKER_EXISTS(self):
        """Getter for attribute of the same name.

        Returns:
            bool: 'True' if tracker file has been open since the initialisation 
                of this object
        """

        return self.__TRACKER_EXISTS

    @property
    def TRACKER_COUNT_ROWS(self):
        """Getter for attribute of the same name.

        Returns:
            int: the number of rows in the global tracker file
        """

        return self.__TRACKER_COUNT_ROWS

    @property
    def TRACKER_COUNT_COLUMNS(self):
        """Getter for attribute of the same name.

        Returns:
            int: the number of columns in the global tracker file
        """

        return self.__TRACKER_COUNT_COLUMNS

    def set_TRACKER_EXISTS(self, value):
        """Setter for attribute of the same name.

        Returns:
            bool: the new value of the variable
        """

        self.__TRACKER_EXISTS = value
        return self.__TRACKER_EXISTS

    def set_TRACKER_COUNT_ROWS(self, value):
        """Setter for attribute of the same name.

        Returns:
            int: the new value of the variable
        """

        self.__TRACKER_COUNT_ROWS = value
        return self.__TRACKER_COUNT_ROWS

    def set_TRACKER_COUNT_COLUMNS(self, value):
        """Setter for attribute of the same name.

        Returns:
            int: the new value of the variable
        """

        self.__TRACKER_COUNT_COLUMNS = value
        return self.__TRACKER_COUNT_COLUMNS


    def add_file(self, fileName, healthStatus=const.untested):
        """Adds a given file with an health status to the tracker file.

        Checks if the file has already been recorded. If not then the file gets 
        added. If it has already been recorded, the entry is updated.

        Args:
            fileName (str): name of file to be added to the tracker file
            healthStatus (int, optional): health status associated with the file. 
                Defaults to const.untested.

        Returns:
            bool: 'True' if file has been added successfully. 'False' otherwise
        """

        if self.is_file_recorded(fileName):
            print("File has already been recorded, repeated entry not added: ", 
                    fileName)
            self.change_health_status(fileName, healthStatus)
        else:
            self.__add_row(fileName)
            self.write_to_file(fileName, 1, healthStatus)
            return True
        return False

    def add_metric(self, operation):
        """Adds a column to the global tracker file and populates it with values 
        returned from the 'operation' method.

        Iterates through each line and saves the data in a list. For the header, 
        the name of the new heading gets appended, and for every other row, the 
        value of the metric gets appended. Then the data get written back to the 
        tracker file.

        Args:
            operation (method (str)): the method that calculates the metric for 
                the entry

        Returns:
            int: 1 to signify completion of method
        """

        with open(const.TRACKER_FILEPATH) as f: # read only
            tracker_file = csv.reader(f)

            # if heading not in top row, add heading
            if operation(heading=True) not in f.read():
                f.seek(0)

                # for tracking during loop
                fileData = []

                for row in tracker_file:

                    # ignore blank rows
                    if len(row) < const.TRACKER_BARE_MINIMUM_LENGTH:
                        continue

                    # add another empty column, and a new heading only if on the first line
                    fileData.append(list(row))
                    if tracker_file.line_num == 1:
                        fileData[0].append(operation(heading=True))
                    else:
                        fileData[-1].append("")

                with open(const.TRACKER_FILEPATH, "w", newline="") as f: # writeable
                    tracker_file = csv.writer(f)
                    tracker_file.writerows(fileData) # write amended data to tracker file

                self.set_TRACKER_COUNT_COLUMNS(self.TRACKER_COUNT_COLUMNS + 1)

        return self.populate_metric(operation)

    def get_column_number(self, columnHeading):
        """Returns the column number associated with a given heading.

        Opens the tracker file, and iterates through the first row to find a 
        match. If found, the index of the column is returned. Else, a 
        ValueError is raised.

        Args:
            columnHeading (str): name of column to be found

        Raises:
            ValueError: raised if the column is not found in the header

        Returns:
            int: index of column
        """

        with open(const.TRACKER_FILEPATH) as f:
            tracker_file = csv.reader(f)

            # find column number
            columnNumber = 0
            for row in tracker_file:
                for heading in row:
                    if heading == columnHeading:
                        return columnNumber # stop when heading is found
                    else:
                        columnNumber += 1
                raise ValueError("Column heading not found")

    def populate_metric(self, operation):
        """Populates/updates an existing metric column in the global tracker 
        file with values returned from the 'operation' method.

        First determines which column needs to be updated by reading the header. 
        Then iterates through each line and overwrites the data in the relevant 
        column.

        Args:
            operation (method (str)): the method that calculates the metric for 
                the entry

        Returns:
            int: 1 to signify completion of method, 0 otherwise
        """

        self.remove_deleted()

        with open(const.TRACKER_FILEPATH) as f: # read only
            tracker_file = csv.reader(f)

            columnHeading = operation(heading=True)
            
            # get column number of given header
            try:
                columnNumber = self.get_column_number(columnHeading)
            except ValueError as e: # if column not found
                print(e)
                return 0

            next(f)

            for row in tracker_file:

                # ignore blank rows
                if len(row) < const.TRACKER_BARE_MINIMUM_LENGTH:
                    continue

                self.write_to_file(row[0], columnNumber, operation(row[0]))

        return 1

    def remove_deleted(self):
        """Removes any files from the tracker file if they have been deleted 
        from the data directory.

        Iterates through the tracker file, and for each file recorded in the 
        global tracker, attempts to find it within the data directory. If 
        successful, the row in the tracker file gets appended to a list. At the 
        end, the list gets written back to the file.

        Returns:
            bool: signifies completion of method
        """

        with open(const.TRACKER_FILEPATH) as f: # read only
            tracker_file = csv.reader(f)

            # for tracking during loop
            fileData = []
            deleted = 0

            for row in tracker_file:
                # skip blank lines
                if len(row) < const.TRACKER_BARE_MINIMUM_LENGTH:
                        continue

                if tracker_file.line_num > 1: # don't try to locate header

                    # get file name from row
                    fileName = row[0]
                    filePath = const.DATA_DIRECTORY + fileName[const.LENGTH_OF_DATA_DIR:]

                    # try to open file
                    try:
                        g = open(filePath)
                    except FileNotFoundError:
                        print("Deleted: ", fileName)
                        deleted += 1
                    else:
                        g.close()
                        fileData.append(list(row)) # if found, add it to list
                else:
                    fileData.append(list(row)) # add header to list

        if deleted > 0:
            with open(const.TRACKER_FILEPATH, "w", newline="") as f: # writeable
                tracker_file = csv.writer(f)
                tracker_file.writerows(fileData) # rewrite data to tracker file
            
            self.set_TRACKER_COUNT_ROWS(self.TRACKER_COUNT_ROWS-deleted)

            print("Deleted {} files".format(deleted))

        return True

    def remove_metric(self, columnHeading):
        """Removes a column from the tracker file.

        Determines which column has the given heading. Then, iterates through 
        the global tracker file and stores each column as part of a list. The 
        column with heading 'columHeading' is removed from the list. Then the 
        new list gets rewritten to the file, overwriting previous data.

        Args:
            columnHeading (str): name of column to be removed

        Returns:
            bool: signifying successful completion of method
        """

        try:
            columnNumber = self.get_column_number(columnHeading)
        except ValueError as e: # if column not found
            print(e)
            return False

        with open(const.TRACKER_FILEPATH) as f: # read only
            tracker_file = csv.reader(f)

            # for tracking during loop
            fileData = []

            for row in tracker_file:
                # skip blank lines
                if len(row) < const.TRACKER_BARE_MINIMUM_LENGTH:
                        continue

                rowData = list(row)
                del rowData[columnNumber]
                
                fileData.append(rowData)


        with open(const.TRACKER_FILEPATH, "w", newline="") as f: # writeable
            tracker_file = csv.writer(f)
            tracker_file.writerows(fileData) # rewrite data to tracker file
        
        self.set_TRACKER_COUNT_COLUMNS(self.TRACKER_COUNT_COLUMNS-1)

        print("Deleted column", columnNumber)

        return True

    def change_health_status(self, fileName, healthStatus):
        """Changes the health status of a given file in the tracker.

        Args:
            fileName (str): name of file whose entry is to be updated
            healthStatus (int): health status associated with the file

        Returns:
            bool: indicates successful completion of method
        """

        return self.write_to_file(fileName, 1, healthStatus)

    def get_health_status(self, fileName):
        """Checks if a file is marked as healthy in the global tracker file.

        Healthy is defined as the file having passed all tests, but may or may 
        not have had warnings raised.

        Args:
            fileName (str): name of the file to check health status of

        Returns:
            int: value of health status, or -1 if file not found
        """
    
        with open(const.TRACKER_FILEPATH) as f: 
            tracker_file = csv.reader(f)
            
            # check each line of tracker file to find file - stops when the file has been found
            for row in tracker_file:
                if row[0] == fileName:
                    return int(row[1]) # get the health status of the file
                    
            print("File '{}' not found in tracker".format(fileName))
            return -1
    
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

        if data == None:
            return

        with open(const.TRACKER_FILEPATH, "r") as f: # read only
            tracker_file = csv.reader(f)

            # for tracking during loop
            rowNumber = 0
            fileData = []
            
            for row in tracker_file:
                # ignore blank rows
                if len(row) < const.TRACKER_BARE_MINIMUM_LENGTH:
                    continue

                fileData.append(list(row))
                
                # count non-blank rows until match is found
                if fileData[rowNumber][0] != fileName:
                    rowNumber += 1

            fileData[rowNumber][columnNumber] = data

        with open(const.TRACKER_FILEPATH, "w", newline="") as f: # writeable
            tracker_file = csv.writer(f)
            tracker_file.writerows(fileData) # write amended data to tracker file
        return True


    def __add_row(self, fileName):
        """Private method to add a single row to the bottom of the CSV file.

        Creates an empty list of the correct length, and sets the first 
        element to the file name. This gets appended to the file.

        Args:
            fileName (str): name of the file to be recorded

        Returns:
            int: to signify completion of method
        """

        dataToWrite = [""] * self.TRACKER_COUNT_COLUMNS # one item for each column in file
        dataToWrite[0] = fileName # first element of list is first column of file
        # append data to file
        with open(const.TRACKER_FILEPATH, "a") as f:
            f.write("\n")
            f.write(", ".join(dataToWrite))

        self.set_TRACKER_COUNT_ROWS(self.TRACKER_COUNT_ROWS + 1)

        return 1

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
