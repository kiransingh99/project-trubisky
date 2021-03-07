from . import const
from . import functions
from . import global_tracker
import csv
import os.path




class ProcessedData:

    def __init__(self, overwrite=True, fileName=""):
        self.overwrite = overwrite
        self.fileName = fileName

    @property
    def individual(self):
        return _Individual(self.fileName)

    """
    @property
    def ensemble(self):
        return _Ensemble(self)
    """
    @property
    def metrics(self):
        return _Metrics()

    @property
    def DATA_DIRECTORY(self):
        """Getter for constant of the same name.

        Returns:
            str: the path to the directory that stores the data files
        """
        
        return const.DATA_DIRECTORY


    def create_all_processed_data_files(self): # DOCSTRING
        for entry in os.listdir(self.DATA_DIRECTORY):
            rawFilePath = os.path.join(self.DATA_DIRECTORY, entry)
            rawFileName = rawFilePath[const.PATH_LENGTH_TO_DATA_DIR:]

            # only check raw data files if they've been marked as healthy
            if entry[:len(const.RAW_DATA_PREFIX)] == const.RAW_DATA_PREFIX:
                G = global_tracker.GlobalFile(False)
                if G.get_health_status(rawFileName) >= const.passedWithWarnings:

                     # if overwrite is False, it doesn't matter if the file has already been recorded
                    if not self.overwrite:
                        processedFilePath = const.DATA_DIRECTORY + \
                            const.PROCESSED_DATA_PREFIX + \
                            entry[len(const.RAW_DATA_PREFIX):]
            
                        try:
                            f = open(processedFilePath)
                        except:
                            pass
                        else:
                            f.close()
                            continue

                    self.create_single_processed_data_file(rawFileName)
        return 1

    def create_single_processed_data_file(self, rawFileName): # DOCSTRING
        fileName = rawFileName.split("\\")[-1][const.LENGTH_OF_DATA_DIR-2:]

        processedFileName = "\\" + rawFileName.split("\\")[1] + "\\" + \
                            const.PROCESSED_DATA_PREFIX + fileName

        rawFilePath = const.DATA_DIRECTORY + rawFileName[const.LENGTH_OF_DATA_DIR:]
        processedFilePath = const.DATA_DIRECTORY + processedFileName[const.LENGTH_OF_DATA_DIR:]

        with open(rawFilePath) as f:
            with open(processedFilePath, "w") as g:
                g.write(",".join(const.COLUMN_HEADERS))
                g.write("\n")
                for line in f:
                    g.write(line)
            G = global_tracker.GlobalFile(False)
            G.write_to_file(rawFileName, 2, processedFileName)

        return processedFileName
      
    def get_all_processed_files(self): # DOCSTRING
        files = []
        for entry in os.listdir(self.DATA_DIRECTORY):
            # filter by processed data files
            if entry[:len(const.RAW_DATA_PREFIX)] == const.PROCESSED_DATA_PREFIX:
                files.append(functions.add_data_directory(entry))

        return files



class _Individual:
    # for writing to and reading from individual pro files
    def __init__(self, fileName):
        self.fileName = fileName

    @property
    def calculations(self):
        return _Calculations(self.fileName)


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

    @property
    def raw_file_name(self): # DOCSTRING
        
        return functions.processed_to_raw(self.fileName)

    def set_file_name(self, value):
        """Setter for the attribute of the same name.

        Args:
            value (str): name of the file to calculate metric(s) for

        Returns:
            str: the new value of the attribute
        """

        self.fileName = value
        return self.fileName

    
    def add_column(self, operation): # DOCSTRING

        with open(self.file_path) as f: # read only
            processed_file = csv.reader(f)

            # if heading not in top row, add heading
            if operation(heading=True) not in f.read():
                f.seek(0)

                # for tracking during loop
                fileData = []

                for row in processed_file:

                    # ignore blank rows
                    if len(row) < const.NUMBER_OF_COLUMNS:
                        continue

                    # add another empty column, and a new heading only if on the first line
                    fileData.append(list(row))
                    if processed_file.line_num == 1:
                        fileData[0].append(operation(heading=True))
                    else:
                        fileData[-1].append("")

                with open(self.filePath, "w", newline="") as f: # writeable
                    processed_file = csv.writer(f)
                    processed_file.writerows(fileData) # write amended data to tracker file

        return self.populate_column(operation)


    def populate_column(self, operation): # DOCSTRING

        values = operation(self.fileName) # needs to return a list with the same length as number of rows in the file

        columnHeading = operation(heading=True)
        
        # get column number of given header
        try:
            columnNumber = self.get_column_number(columnHeading)
        except ValueError as e: # if column not found
            print(e)
            return 0

        self.write_to_file(columnNumber, values)

        return 1

    def get_column_number(self, columnHeading): # COMPLETE, DOCSTRING

        with open(self.file_path) as f:
            processed_file = csv.reader(f)

            # find column number
            columnNumber = 0
            for row in processed_file:
                for heading in row:
                    if heading == columnHeading:
                        return columnNumber # stop when heading is found
                    else:
                        columnNumber += 1
                raise ValueError("Column heading not found")


    def write_to_file(self, columnNumber, data): # COMPLETE, DOCSTRING

        with open(self.file_path, "r") as f: # read only
            processed_file = csv.reader(f)

            # for tracking during loop
            fileData = []
            
            for i, row in enumerate(processed_file):
                # ignore blank rows
                if len(row) < const.NUMBER_OF_COLUMNS:
                    continue

                fileData.append(list(row))
                if i > 0: # skip header
                    fileData[i][-1] = data[i]

        with open(self.file_path, "w", newline="") as f: # writeable
            tracker_file = csv.writer(f)
            tracker_file.writerows(fileData) # write amended data to tracker file
        return True

    def get_health_status(self): # DOCSTRING
        """Checks if a file has been marked as healthy..

        Args:
            fileName (str): name of file to check

        Returns:
            int: Health status of a file
        """

        rawFileName = self.raw_file_name

        G = global_tracker.GlobalFile(fullInitialisation = False)
        return G.get_health_status(rawFileName)


class _Calculations:
    def __init__(self, fileName=""):
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

    def duplicate(self, fileName=None, heading=False):
        if heading:
            return "duplicate" # title of column in tracker file

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)
    
        data = []

        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                # get to end of file
                for row in csv_file:
                    data.append(row[0])
                return data
        except:
            print("Couldn't open file:", fileName)
            print("Try again if you think this is a mistake.")



"""
class _Ensemble:
    # for comparing/ analysing data from all files - reads global tracker and 
    # produces graphs
    def init(self):
        pass

"""


class _Metrics:
    # for calculating metrics, accessed via global tracker file
    def init(self, fileName=""):

        self.fileName = functions.raw_to_processed(fileName)
    
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


    # metrics for tracker

    def total_time(self, fileName=None, heading=False):
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
            print("Couldn't open file:", fileName)
            print("Try again if you think this is a mistake.")

    def spiral_rate(self, fileName=None, heading=False): # DOCSTRING
        if heading:
            return "spiral rate" # title of column in tracker file

        if fileName == None:
            fileName = functions.raw_to_processed(self.fileName)
        else:
            self.set_file_name(functions.raw_to_processed(fileName))
    
        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                columnNumber = self.get_column_number("w (e_r)")
                max = 0
                next(f) # skip header
                for row in csv_file:
                    if abs(float(row[columnNumber])) > max:
                        max = abs(float(row[columnNumber]))
                return max
        except FileNotFoundError:
            print("Couldn't open file:", fileName)
            print("Try again if you think this is a mistake.")


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

        with open(self.filePath) as f:
            processed_file = csv.reader(f)

            # find column number
            columnNumber = 0
            for row in processed_file:
                for heading in row:
                    if heading == columnHeading:
                        return columnNumber # stop when heading is found
                    else:
                        columnNumber += 1
                raise ValueError("Column heading not found")
