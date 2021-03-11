from . import const
from . import functions
from . import global_tracker
import csv
import matplotlib.pyplot as plt
import numpy as np
import os

class ProcessedData:
    """Main class for handling the processed data files based on the raw data 
    received from the ball, and conducting any analysis.

    The methods of this class are divided into four sections:
        - main (the methods of this class): creates the processed data files and 
        handles tasks to do with the files as a whole
        - "individual": does the tasks related to individual processed data 
        files, including formatting and calculations
        - "ensemble" : TO DO
        - "metrics": calculates the metrics for the global tracker file based on 
        the contents of the processed data file

    Attributes:
        overwrite (bool): set as 'True' if data in the processed data files 
            should be overwritten with changes otherwise set as 'False'.
        fileName (str): name of the processed data file to be worked on.
        
    Methods:
        __init__ : class constructor.
        ensemble (property) : TO DO
        individual (property) : groups the 'individual' methods.
        metrics (property) : groups the 'metric' methods.
        DATA_DIRECTORY (property) : returns the constant of the same names. 
            Takes its value from the const.py file.
        create_all_processed_data_files : creates processed data files for all 
            raw data files marked as healthy.
        create_single_processed_data_file : creates a processed data file for 
            any one raw data file.
        get_all_processed_files : gets a list of all the processed data files 
            created.
    """

    def __init__(self, overwrite=True, fileName=""):
        """Constructor for class, defines constants and class attributes.

        Args:
            overwrite (bool): whether or not to overwrite processed data files.
            fileName (str): the name of the processed data file to work on.
        """

        self.overwrite = overwrite

        # ensure processed file, not raw
        self.fileName = functions.raw_to_processed(fileName)

    """
    @property
    def ensemble(self): # DOCSTRING
        return _Ensemble(self)
    """

    @property
    def individual(self):
        """Creates instance of _Individual as an object of ProcessedData.
        
        Creates an instance of the '_Individual' class as an object called 
        'self.individual', where 'self' is the name of the instance of 
        'ProcessedData'. Parameters passeed to '_Individual' are as set by the 
        'ProcessedData' class attributes.

        Returns:
            _Individual object: instance of class.
        """

        return _Individual(self.fileName)

    @property
    def metrics(self):
        """Creates instance of _Metrics as an object of ProcessedData.
        
        Creates an instance of the '_Metrics' class as an object called 
        'self.individual', where 'self' is the name of the instance of 
        'ProcessedData'. Parameters passeed to '_Metrics' are as set by the 
        'ProcessedData' class attributes.

        Returns:
            _Metrics object: instance of class.
        """

        return _Metrics()

    @property
    def DATA_DIRECTORY(self):
        """Getter for constant of the same name. Path to the directory that 
        stores the data files.

        Returns:
            str: the path to the directory that stores the data files.
        """
        
        return const.DATA_DIRECTORY


    def create_all_processed_data_files(self):
        """Creates a processed data file for every raw data file that has been 
        marked as healthy in the global tracker file.

        Iterates through every file in the data directory and picks out the 
        healthy raw data files. If the processed data file for the raw data file 
        does not exist, or if overwrite is set 'True', the processed file gets
        created and populated. If the file exists and overwrite is set 'False', 
        the entry is skipped.

        Returns:
            int: number of files created.
        """

        count = 0

        # iterate over every file in the data directory
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
            
                        # check file exists
                        try:
                            f = open(processedFilePath)
                        except FileNotFoundError:
                            pass
                        else:
                            # if it exists, close file and move on
                            f.close()
                            continue

                    self.create_single_processed_data_file(rawFileName)
                    count += 1

        print("Finished: {} processed data files created".format(count))
        return count

    def create_single_processed_data_file(self, rawFileName):
        """Creates a processed data file for any given raw data file.

        Stores the from the raw data file in an array, removes any offset from 
        the sensors, and changes the units of the data to make it more usable. 
        Then writes this amended dataset to the corresponding processed data 
        file.

        Args:
            rawFileName (str): name of the raw data file.

        Returns:
            str: name of the new processed data file.
        """

        fileName = rawFileName.split("\\")[-1][const.LENGTH_OF_DATA_DIR-2:]

        processedFileName = "\\" + rawFileName.split("\\")[1] + "\\" + \
                            const.PROCESSED_DATA_PREFIX + fileName

        rawFilePath = const.DATA_DIRECTORY + rawFileName[const.LENGTH_OF_DATA_DIR:]
        processedFilePath = const.DATA_DIRECTORY + processedFileName[const.LENGTH_OF_DATA_DIR:]

        try:
            with open(rawFilePath) as f:
                raw_file = csv.reader(f)
                with open(processedFilePath, "w") as g:
                    header = ",[raw] ".join(const.COLUMN_HEADERS)
                    g.write(header)
                    g.write("\n")

                    sensorsInitialised = [False, False, False]
                    allSensorsInitialised = False
                    
                    for line in raw_file:
                        if not allSensorsInitialised:
                            if line[1:4] != ["0.00", "0.00", "0.00"]:
                                sensorsInitialised[0] = True
                            if line[4:7] != ["0.00", "0.00", "0.00"]:
                                sensorsInitialised[1] = True
                            if line[7:10] != ["0.00", "0.00", "0.00"]:
                                sensorsInitialised[2] = True
                            if sensorsInitialised == [True, True, True]:
                                allSensorsInitialised = True

                        newData = self.__convert_units(line, sensorsInitialised)
                        g.write(",".join(newData))
                        g.write("\n")
                G = global_tracker.GlobalFile(False)
                G.write_to_file(rawFileName, 2, processedFileName)
            print("  Created " + processedFileName)
            return processedFileName
        except FileNotFoundError as e:
            print("Raw data file could not be found:", e)
      
    def get_all_processed_files(self):
        """Returns a list of all processed data files in the data directory.

        Iterates through the directory, and if the prefix matches the form of 
        the processed data files, then add the name of the file to a list.

        Returns:
            list[str]: names of processed data files
        """

        files = []
        for entry in os.listdir(self.DATA_DIRECTORY):
            # filter by processed data files
            if entry[:len(const.RAW_DATA_PREFIX)] == const.PROCESSED_DATA_PREFIX:
                files.append(functions.add_data_directory(entry))

        return files

    def __convert_units(self, data, sensorsInitialised):
        """Converts the units of the raw data file to ones that are more 
        appropriate for the usage.

        Args:
            data (list[str]): a line of data read from the raw data file.
            sensorsInitialised (list[bool]): tracks whether each sensor has been 
                initialised yet, and therefore if it is outputting values.

        Returns:
            list[str]: the data in the correct units for the processed data 
                file.
        """

        # convert data from strings into numerical values
        for i in range(len(data)):
            if i == 0:
                data[i] = int(data[i])
            else:
                data[i] = float(data[i])
        
        # subtract offsets
        if sensorsInitialised[0]:
            data[1:4] = np.subtract(data[1:4], const.SENSOR_OFFSETS[1:4])
        if sensorsInitialised[1]:
            data[4:7] = np.subtract(data[4:7], const.SENSOR_OFFSETS[4:7])
        if sensorsInitialised[2]:
            data[7:10] = np.subtract(data[7:10], const.SENSOR_OFFSETS[7:10])

        # change the units
        newData = []
        
        newData.append(data[0]) # time stays in milliseconds
        newData.extend(data[1:4]) # linear acceleration stays in m/s^2
        newData.extend(data[4:7]) # angular velocity stays in rad/s
        newData.extend(np.deg2rad(data[7:])) # euler angles change from degrees to radians

        # convert each element back into a string
        for i in range(len(data)):
            newData[i] = str(newData[i])

        return newData



class _Individual:
    """Handles all the tasks related to individual processed data files, 
    including formatting and calculations.

    The methods of this class are divided into two sections:
        - main (the methods of this class): focuses on the formatting and 
        structure of the files
        - "calculations": does calculations based on the data in the files

    Attributes:
        fileName (str): name of the processed data file to be worked on.
        filePath (str): full file path to the given processed data file.
        
    Methods:
        __init__ : class constructor.
        calculations (property) : groups the 'calculations' methods.
        file_path (property) : getter for the attribute of the same name.
        raw_file_name (property) : getter for the name of the raw day file 
            corresponding to the processed data file.
        set_file_name : setter for attribute of the same name.
        add_column : adds a new column to the processed data file.
        get_column_number : returns the column number of a given heading.
        get_health_status : checks if a raw data file is marked as healthy in 
            the global tracker.
        populate_column : populates/ updates an existing column in the processed 
            data file.
        write_to_file : overwrites an entry already listed in the file.
    """

    def __init__(self, fileName):
        """Constructor for class.

        Args:
            fileName (str): name of the processed data files
        """

        self.fileName = fileName

    @property
    def calculations(self):
        """Creates instance of _Calculations as an object of _Individual.
        
        Creates an instance of the '_Calculations' class as an object 
        called 'self.calculations', where 'self' is the name of the instance of 
        '_Individual'. Parameters passeed to '_Calculations' are as set by the 
        '_Individual' class attributes.

        Returns:
            _Calculations object: instance of class
        """
        
        return _Calculations(self.fileName)

    @property
    def file_path(self):
        """Getter for the attribute of the same name. Path to the processed data 
        file.

        Assigns the value first, by adding the full file path to 
        'self.fileName'.

        Returns:
            str: path to the raw data file.
        """
        
        self.filePath = const.DATA_DIRECTORY + self.fileName[const.LENGTH_OF_DATA_DIR:]
        return self.filePath

    @property
    def raw_file_name(self):
        """Getter for the name of the raw data file corresponding to the 
        processed data file.

        Returns:
            str: name of raw data file corresponding to the processed data file.
        """
        
        return functions.processed_to_raw(self.fileName)


    def set_file_name(self, value):
        """Setter for the attribute of the same name.Name of the processed data 
        file.

        Args:
            value (str): name of the file to calculate metric(s) for.

        Returns:
            str: the new value of the attribute.
        """

        self.fileName = functions.raw_to_processed(value)
        return self.fileName

    
    def add_column(self, operation):
        """Adds another column to the processed data file and populates it with 
        values returned from the 'operation' method.

        First checks what the operation is - for all operations this method 
        iterates once, but for 'smooth', it iterates 10 times, one for each 
        column. Iterates through each line and saves the data in a list. For the 
        header, the name of the new heading gets appended, and for every other 
        row, the value from the operation gets appended. Then the data get 
        written back to the processed data file.

        Args:
            operation (method (str)): the method that calculates the metric for 
                the entry.

        Returns:
            int: 1 to signify completion of method.
        """

        header = operation(heading=True)
        if operation.__name__ == "smooth":
            iterations = len(const.COLUMN_HEADERS)
        else:
            iterations = 1

        for i in range (1, iterations):

            header = operation(heading=True)

            with open(self.file_path) as f: # read only
                processed_file = csv.reader(f)

                # if heading not in top row, add heading
                if "," + header not in next(f):
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
                            fileData[0].append(header)
                        else:
                            fileData[-1].append("")

                    with open(self.filePath, "w", newline="") as f: # writeable
                        processed_file = csv.writer(f)
                        processed_file.writerows(fileData) # write amended data to tracker file
                
                self.populate_column(operation)

    def delete_file(self, filePath): #COMPLETE, DOCSTRING

        filePath = functions.raw_to_processed(filePath)
        if os.path.exists(filePath):
            os.remove(filePath)
            return 1
        else:
            return 0

    def get_column_number(self, columnHeading):
        """Returns the column number associated with a given heading.

        Opens the processed data file, and iterates through the first row to 
        find a match. If found, the index of the column is returned. Else, a 
        ValueError is raised.

        Args:
            columnHeading (str): name of column to be found.

        Raises:
            ValueError: raised if the column is not found in the header.

        Returns:
            int: index of column.
        """

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

    def get_health_status(self):
        """Gets the health status of the raw data file corresponding to the 
        given processed data file.

        Returns:
            int: Health status of a file.
        """

        rawFileName = self.raw_file_name

        G = global_tracker.GlobalFile(fullInitialisation = False)
        return G.get_health_status(rawFileName)

    def graph_sensor_data(self, filtered=True, unfiltered=True): # COMPLETE, DOCSTRING
        if not filtered and not unfiltered:
            print("No data to be plotted. Check parameters.")
            return None
        
        for i in range(0, 7, 3):
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                time = []
            
                data =  [[] for j in range(3 * (filtered+unfiltered))]
                for row in csv_file:
                    if csv_file.line_num == 1:
                        time.append(row[0])
                        if unfiltered:
                            data[-3].append(row[i+1])
                            data[-2].append(row[i+2])
                            data[-1].append(row[i+3])
                        if filtered:
                            data[0].append(row[i+10])
                            data[1].append(row[i+11])
                            data[2].append(row[i+12])
                    else:
                        time.append(float(row[0]))
                        if unfiltered:
                            data[-3].append(float(row[i+1]))
                            data[-2].append(float(row[i+2]))
                            data[-1].append(float(row[i+3]))
                        if filtered:
                            data[0].append(float(row[i+10]))
                            data[1].append(float(row[i+11]))
                            data[2].append(float(row[i+12]))

                #plot linear acceleration and angular velocity separately
                fig, (er, e1, e2) = plt.subplots(3, sharex=True)
                if unfiltered:
                    er.plot(time[1:], data[-3][1:], label=data[-3][0])
                    e1.plot(time[1:], data[-2][1:], label=data[-2][0])
                    e2.plot(time[1:], data[-1][1:], label=data[-1][0])
                if filtered:
                    er.plot(time[1:], data[0][1:], label=data[0][0])
                    e1.plot(time[1:], data[1][1:], label=data[1][0])
                    e2.plot(time[1:], data[2][1:], label=data[2][0])

                if filtered and unfiltered:
                        fig.suptitle("Filtered and Unfiltered Sensor Data Against Time")
                elif filtered:
                    fig.suptitle("Filtered Sensor Data against Time")
                elif unfiltered:
                    fig.suptitle("Unfiltered Sensor Data against Time")
                er.legend()
                e1.legend()
                e2.legend()
                fig.show()           

        return 1


    def populate_column(self, operation):
        """Populates/updates an existing column in the processed data file with 
        values returned from the 'operation' method.

        First determines which column needs to be updated by reading the header. 
        Then iterates through each line and overwrites the data in the relevant 
        column.

        Args:
            operation (method (str)): the method that calculates the values for 
                the entry.

        Returns:
            int: 1 to signify completion of method, 0 otherwise.
        """

        columnHeading = operation(heading=True)
        values = operation(self.fileName)
        
        # get column number of given header
        try:
            columnNumber = self.get_column_number(columnHeading)
        except ValueError as e: # if column not found
            print(e)
            return 0

        self.write_to_file(columnNumber, values)

        return 1

    def write_to_file(self, columnNumber, data):
        """Writes the data passed to this method to a given column in the 
        processed data file.
        
        Saves the data in the file as a list, and adds the data to the list, 
        before writing the list back to the file.

        Args:
            columnNumber (int): the column in the row to be overwritten.
            data list[(any)]: data to write into file, elements get cast into a 
                string.

        Returns:
            bool: signifies complete execution of method.
        """

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
                    fileData[i][columnNumber] = data[i]

        with open(self.file_path, "w", newline="") as f: # writeable
            tracker_file = csv.writer(f)
            tracker_file.writerows(fileData) # write amended data to tracker file
        return True


class _Calculations:
    """Handles all the tasks related to individual processed data files, 
    including formatting and calculations.

    The methods of this class are divided into two sections:
        - main (the methods of this class): focuses on the formatting and 
        structure of the files
        - "calculations": does calculations based on the data in the files

    Attributes:
        fileName (str): name of the processed data file to be worked on.
        filePath (str): full file path to the given processed data file.
        columnNumber (int): the number of the column to smooth (should be 
            between 1 and 10 inclusive).
        
    Methods:
        __init__ : class constructor.
        file_path (property) : getter for the attribute of the same name.
        set_file_name : setter for attribute of the same name.
        smooth : runs the raw sensor data through a low pass filter to smooth 
            it.
    """

    def __init__(self, fileName=""):
        """Constructor for class.

        Args:
            fileName (str, optional): name of file to do calculations on. 
                Defaults to "".
        """
        self.fileName = fileName
        self.columnNumber = 1
    
    @property
    def file_path(self):
        """Getter for the attribute of the same name.

        Assigns the value first, by adding the full file path to 
        'self.fileName'.

        Returns:
            str: path to the raw data file.
        """
        
        self.filePath = const.DATA_DIRECTORY + self.fileName[const.LENGTH_OF_DATA_DIR:]
        return self.filePath


    def set_file_name(self, value):
        """Setter for the attribute of the same name.

        Args:
            value (str): name of the file to calculate metric(s) for.

        Returns:
            str: the new value of the attribute.
        """

        self.fileName = functions.raw_to_processed(value)
        return self.fileName


    def smooth(self, fileName=None, heading=False):
        """Smoothens one of the columns of the processed data file and adds the 
        data as a new column.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the values for this column are 
        calculated.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to actually calculate the value. Defaults to 
                False.

        Returns:
            list[float]: smoothed values of the same dimension as the input 
                data.
        """


        if self.columnNumber == const.NUMBER_OF_COLUMNS:
            self.columnNumber = 1

        columnNumber = self.columnNumber

        if heading:
            return const.COLUMN_HEADERS[columnNumber]

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)
        
        data = []

        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                for row in csv_file:
                    if csv_file.line_num == 1: # header row
                        data.append(0) # append any numerical value - this will be discarded
                    else:
                        data.append(float(row[columnNumber]))
        except FileNotFoundError:
            print("Couldn't open file:", fileName)
        else:
            windowSize = 4
            smoothed = functions.moving_average(data, windowSize)

            self.columnNumber += 1
            

            return [0] * (windowSize-1) + list(smoothed)


    def duplicate(self, fileName=None, heading=False): # DUMMY FUNCTION
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
                for row in csv_file:
                    data.append(row[0])
                return data
        except:
            print("Couldn't open file:", fileName)



"""
class _Ensemble: # DOCSTRING
    # for comparing/ analysing data from all files - reads global tracker and 
    # produces graphs
    def init(self): # DOCSTRING
        pass

"""


class _Metrics:
    """Object that calculates all the metrics for the global tracker.

    Attributes:
        fileName (str) : name of the file to calculate the metric for
        filePath (str) : file path to the file which will be operated on

    Methods:
        __init__ : constructor for class
        file_path (property) : getter for the attribute of the same name
        set_file_name : setter for the attribute of the same name
        all : runs all methods in this class that calculate a metric
        total_time : metric calculator for the time of the throw recorded
    """

    def init(self, fileName=""):
        """Constructor for class. Determines the processed data file name from 
        the raw data file name 

        Args:
            fileName (str, optional): Name of file to calculate metrics for. 
                Defaults to "".
        """

        self.fileName = functions.raw_to_processed(fileName)
    
    @property
    def file_path(self):
        """Getter for the attribute of the same name. Path to the processed data 
        file.

        Assigns the value first, by adding the full file path to 
        'self.fileName'.

        Returns:
            str: path to the raw data file.
        """
        
        self.filePath = const.DATA_DIRECTORY + self.fileName[const.LENGTH_OF_DATA_DIR:]
        return self.filePath


    def set_file_name(self, value):
        """Setter for the attribute of the same name. Name of the processed data 
        file.

        Args:
            value (str): name of the file to calculate metric(s) for.

        Returns:
            str: the new value of the attribute.
        """

        self.fileName = functions.raw_to_processed(value)
        return self.fileName


    def get_column_number(self, columnHeading):
        """Returns the column number associated with a given heading.

        Opens the tracker file, and iterates through the first row to find a 
        match. If found, the index of the column is returned. Else, a 
        ValueError is raised.

        Args:
            columnHeading (str): name of column to be found.

        Raises:
            ValueError: raised if the column is not found in the header.

        Returns:
            int: index of column.
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


    def total_time(self, fileName=None, heading=False):
        """Calculates a metric (total time of recording) for a given throw.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, each file listed is found, and the 
        metric is calculated for it.

        Args:
            fileName (str): name of the file to calculate the metric for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to actually calculate the value. Defaults to 
                False.

        Returns:
            int: value of metric.
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

    def spiral_rate(self, fileName=None, heading=False):
        """Calculates a metric (rate of the spiral) for a given throw.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, each file listed is found, and the 
        metric is calculated for it.

        Args:
            fileName (str): name of the file to calculate the metric for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to actually calculate the value. Defaults to 
                False.

        Returns:
            int: value of metric.
        """

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
