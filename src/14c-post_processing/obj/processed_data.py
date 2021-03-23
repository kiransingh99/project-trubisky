from . import const
from .exceptions import UniqueCaseException
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
        DATA_DIRECTORY (property) : getter for the constant of the same names. 
            Takes its value from the const.py file.
        file_name (property) : getter for the attribute of the same name.
        set_file_name : setter for the attribute of the same name.
        create_all_processed_data_files : creates processed data files for all 
            raw data files marked as healthy.
        create_single_processed_data_file : creates a processed data file for 
            any one raw data file.
        get_all_processed_files : gets a list of all the processed data files 
            created.
        __convert_units : changes the units of the sensor output to make 
            calculations easier.
        __ write_data_to_file : writes a column of data to processed data file.
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

        return _Individual(self.file_name)

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

    @property
    def file_name(self):
        """Getter for the arribute of the same name. Name of the processed data 
        file.

        Returns:
            str: name of processed data file.
        """

        return self.fileName

    
    def set_file_name(self, value):
        """Setter for the attribute of the same name. Name of the processed data 
        file.

        Args:
            value (str): new value for attribute.

        Returns:
            str: new value of attribute.
        """
        self.fileName = value
        return self.fileName


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

        # get raw and processed data file names
        fileName = rawFileName.split("\\")[-1][const.LENGTH_OF_DATA_DIR-2:]
        processedFileName = "\\" + rawFileName.split("\\")[1] + "\\" + \
                            const.PROCESSED_DATA_PREFIX + fileName
        rawFilePath = const.DATA_DIRECTORY + rawFileName[const.LENGTH_OF_DATA_DIR:]
        processedFilePath = const.DATA_DIRECTORY + processedFileName[const.LENGTH_OF_DATA_DIR:]

        # check files exists
        try:
            f = open(rawFilePath)
        except FileNotFoundError as e:
            print("Raw data file could not be found:", e)
            return

        raw_file = csv.reader(f)
        self.set_file_name(processedFileName)
        
        try:
            g = open(processedFilePath, "w")
        except FileNotFoundError as e:
            print("Processed data file could not be found:", e)

        # add header, but prefix all sensor columns with '[raw]
        header = ",[raw] ".join(const.COLUMN_HEADERS)
        g.write(header)
        g.write("\n")

        # process sensor data only if sensors have initialised
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

        # close raw and processed data files
        g.close()
        f.close()

        # calculate timesteps between samples and write to file
        self.individual.add_column(self.individual.calculations.delta_time)
        
        # add name of processed data file to tracker
        G = global_tracker.GlobalFile(False)
        G.write_to_file(rawFileName, 2, processedFileName)
        
        print("  Created " + processedFileName)
        return processedFileName
      
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
        for i in range(0, len(data)):
            data[i] = float(data[i])
        
        # subtract offsets
        if sensorsInitialised[0]:
            data[1:4] = np.subtract(data[1:4], const.SENSOR_OFFSETS[1:4])
        else:
            data[1:4] = np.multiply(data[1:4], 0)
        if sensorsInitialised[1]:
            data[4:7] = np.subtract(data[4:7], const.SENSOR_OFFSETS[4:7])
        else:
            data[4:7] = np.multiply(data[4:7], 0)
        if sensorsInitialised[2]:
            data[7:10] = np.subtract(data[7:10], const.SENSOR_OFFSETS[7:10])
        else:
            data[7:10] = np.multiply(data[7:10], 0)

        # change the units
        newData = []
        
        newData.append(data[0]/1000) # time changes from milliseconds to seconds
        newData.extend(data[1:4]) # linear acceleration stays in m/s^2
        newData.extend(np.deg2rad(data[4:7])) # angular velocity changes from deg/s to rad/s
        newData.extend(np.deg2rad(data[7:])) # euler angles change from degrees to radians

        # convert each element back into a string
        for i in range(len(data)):
            newData[i] = str(newData[i])

        return newData

    def __write_data_to_file(self, header, data):
        """Writes a column of data to the processed data file.

        File to write to is decided by the attribute 'fileName'. The contents of 
        the file is stored in a list and the relevant data is appended to the 
        list. Then the new list is written back to the file.

        Args:
            header (str): name of column header.
            data (list[str]): data to write to the file.

        Returns:
            int: '1' signifies successful completion of method.
        """

        filePath = const.DATA_DIRECTORY + self.file_name.split("\\")[-1]

        with open(filePath) as f: # read only
            processed_file = csv.reader(f)

            # for tracking during loop
            fileData = []

            # store first line of file in list - remove line break and split into a list
            fileData.append(f.readline()[:-1].split(","))
            fileData[0].append(header)

            for row in processed_file:
                # ignore blank rows
                if len(row) < const.NUMBER_OF_COLUMNS:
                    continue

                # add another empty column
                fileData.append(list(row))
                fileData[-1].append(str(data[processed_file.line_num-1]))

            with open(filePath, "w", newline="") as f: # writeable
                processed_file = csv.writer(f)
                processed_file.writerows(fileData) # write amended data to tracker file
            
            return 1


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
        delete_file : deletes a given processed data file
        get_column_number : returns the column number of a given heading.
        get_health_status : checks if a raw data file is marked as healthy in 
            the global tracker.
        graph_sensor_data : produces graphs of raw (unfiltered) and/or filtered 
            (smoothened) sensor data.
        populate_column : populates/ updates an existing column in the processed 
            data file.
        write_to_file : overwrites an entry already listed in the file.
        __make_graph : produces a graph based on parameters passed to it.
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

        Removes any existing path from the file, and then prepends the full file 
        path. Assigns the value by adding the full file path to 'self.fileName'.

        Returns:
            str: path to the raw data file.
        """
        
        self.filePath = const.DATA_DIRECTORY + self.fileName.split("\\")[-1]
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

        # exception is thrown upon completion of group operations
        try:
            header = operation(fileName=self.fileName, heading=True)
        except UniqueCaseException:
            return 1

        if operation.__name__ == "smooth":
            iterations = len(const.COLUMN_HEADERS)-1
        else:
            iterations = 1

        for _ in range (0, iterations):
            header = operation(heading=True)

            with open(self.file_path) as f: # read only
                processed_file = csv.reader(f)

                # if heading not in top row, add heading
                if "," + header not in next(f):
                    f.seek(0)

                    # for tracking during loop
                    fileData = []

                    # store first line of file in list - remove line break and split into a list
                    fileData.append(f.readline()[:-1].split(","))
                    fileData[0].append(header)

                    for row in processed_file:
                        # ignore blank rows
                        if len(row) < const.NUMBER_OF_COLUMNS:
                            continue

                        # add another empty column
                        fileData.append(list(row))
                        fileData[-1].append("")

                    with open(self.filePath, "w", newline="") as f: # writeable
                        processed_file = csv.writer(f)
                        processed_file.writerows(fileData) # write amended data to tracker file
                
                self.populate_column(operation)

    def delete_file(self, filePath):
        """Deletes a given processed data file.

        Args:
            filePath (str): path to raw/processed data file

        Returns:
            int: '1' if file was deleted, '0' otherwise
        """

        # ensure we're using processed data file, not raw data
        filePath = functions.raw_to_processed(filePath)

        if os.path.exists(filePath):
            os.remove(filePath)
            return 1
        else:
            return 0

    def get_column_headers(self):
        """Returns a list of all the column headers in any given processed data 
        file.

        Reads the first line of a processed data file, and produces a list of 
        the headings that were read. This list is returned.

        Returns:
            list[str]: list of headers in the file.
        """

        try:
            with open(self.file_path) as f:
                headers = f.readline()[:-1].split(",")
        except FileNotFoundError:
            print("File could not be found")
            return []
        else:
            return headers

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

    def graph(self, x_title, y_titles, title=""):
        """Produces a graph of data in a file, based on the column headers 
        given.

        Checks if the file exists, and if so, reads the headers and data from 
        the relevant columns within it. Data for the vertical axis can have 
        multiple datasets, so data reading is repeated accordingly.


        Args:
            x_title (str): title of column whose data is to be plotted on the 
                horizontal axis
            y_titles (str): titles of columns whose data is to be plotted on the 
                vertical axis.
            title (str, optional): title to display on plot window. If left 
                blank, defaults to '{list of y_titles} against {x_title}'.

        Returns:
            int: signifies successful completion of function
        """

        # check if file exists
        try:
            f = open(self.file_path)
        except FileNotFoundError as e:
            print("Processed data file could not be found:", e)
            return 0

        csv_file = csv.reader(f)

        # create variables to store data - vertical axis may have multiple values
        x_data = []
        y_data =  [[] for title in y_titles]
        columnNumber_x = self.get_column_number(x_title)
        columnNumbers_y = [self.get_column_number(title) for title in y_titles]

        # read first line and add headings to a list
        firstLine = f.readline()[:-1].split(",")
        x_data.append(firstLine[columnNumber_x])
        for i in range(len(y_titles)):
            y_data[i].append(firstLine[columnNumbers_y[i]])
    
        # add data from the rest of the file to the list so it can be plotted
        for row in csv_file:
            x_data.append(float(row[columnNumber_x]))
            for i in range(len(y_titles)):
                y_data[i].append(float(row[columnNumbers_y[i]]))
            
        f.close()

        # generate title if none is given
        if title == "":
            y_labels = ", ".join(y_titles)
            title = "{} against {}".format(y_labels, x_title)

        self.__make_graph(x_data, [y_data], title)

        return 1

    def graph_flight_path(self):
        """Produces a graph showing how height varies with horizontal distance 
        travelled by the ball.

        Opens the processed data file, and creates a list containing all the 
        data to be plotted. Then a method is called to display this dataset to 
        the user.

        Args:
            filtered (bool, optional): set to 'True' if filtered sensor data 
                should be plotted. Set to 'False' otherwise. Defaults to True.
            unfiltered (bool, optional): set to 'True' if unfiltered sensor data 
                should be plotted. Set to 'False' otherwise Defaults to False.

        Returns:
            int: signifies successful completion of method.
        """
        
        try:
            f = open(self.file_path)
        except FileNotFoundError as e:
            print("Processed data file could not be found:", e)
            return 0

        columnNumber_x = self.get_column_number("pos (x)")
        columnNumber_y = self.get_column_number("pos (y)")

        csv_file = csv.reader(f)
        x_data = []
        y_data =  []

        # read first line and add headings to a list
        firstLine = f.readline()[:-1].split(",")
        x_data.append(firstLine[columnNumber_x])
        y_data.append(firstLine[columnNumber_y])
    
        # add data from the rest of the file to the list so it can be plotted
        for row in csv_file:
            x_data.append(float(row[columnNumber_x]))
            y_data.append(float(row[columnNumber_y]))
            
        f.close()

        title = "Flight path of Ball (Height against Distance)"

        self.__make_graph(x_data, [[y_data]], title)

        return 1

    def graph_sensor_data(self, filtered=True, unfiltered=False):
        """Produces graphs of raw (unfiltered) and/or filtered (smoothened) 
        sensor data from the processed data file.

        Opens the processed data file, and depending on the input arguments, 
        creates a list containing all the data to be plotted. Then a method is 
        called to display this dataset to the user.

        Args:
            filtered (bool, optional): set to 'True' if filtered sensor data 
                should be plotted. Set to 'False' otherwise. Defaults to True.
            unfiltered (bool, optional): set to 'True' if unfiltered sensor data 
                should be plotted. Set to 'False' otherwise Defaults to False.

        Returns:
            int: signifies successful completion of method.
        """
        
        if not filtered and not unfiltered:
            print("No data to be plotted. Check parameters.")
            return None

        for i in range(0, 7, 3): # repeat once for each sensor
            try:
                f = open(self.file_path)
            except FileNotFoundError as e:
                print("Processed data file could not be found:", e)
                return 0

            csv_file = csv.reader(f)
            time = []
            # three sublists for filtered data, three for unfiltered
            data =  [[] for j in range(3 * (filtered + unfiltered))]

            # read first line and add headings to a list
            firstLine = f.readline()[:-1].split(",")
            time.append(firstLine[0])
            for j in range(0, 3):
                if unfiltered:
                    data[j-3].append(firstLine[i+j+1])
                if filtered:
                    data[j].append(firstLine[i+len(const.COLUMN_HEADERS)+j+1])
        
            # add data from the rest of the file to the list so it can be plotted
            for row in csv_file:
                time.append(float(row[0]))
                for j in range(0, 3):
                    if unfiltered:
                        data[j-3].append(float(row[i+j+1]))
                    if filtered:
                        data[j].append(float(row[i+len(const.COLUMN_HEADERS)+j+1]))

            f.close()

            y_data = [[] for j in range(3)]
            
            # restructure data for __make_graph method
            for j in range(0, 3):
                if unfiltered:
                    y_data[j].append(data[j-3])
                if filtered:
                    y_data[j].append(data[j])

            if filtered and unfiltered:
                title = "Filtered and Unfiltered Sensor Data Against Time"
            elif filtered:
                title = "Filtered Sensor Data against Time"
            elif unfiltered:
                title = "Unfiltered Sensor Data against Time"

            self.__make_graph(time, y_data, title)

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
        before writing the list back to the file. Note that the first 

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
            
            
            firstLine = f.readline()[:-1].split(",")
            fileData.append(firstLine)

            for i, row in enumerate(processed_file, start=1):
                # ignore blank rows
                if len(row) < const.NUMBER_OF_COLUMNS:
                    continue

                fileData.append(list(row))
                fileData[i][columnNumber] = data[i-1]

        with open(self.file_path, "w", newline="") as f: # writeable
            tracker_file = csv.writer(f)
            tracker_file.writerows(fileData) # write amended data to tracker file
        return True


    def __make_graph(self, x_data, y_data, title=""):
        """Produces a graph based on the data passed in as parameters.

        Capable of producing multiple graphs within one figure, with multiple 
        datasets plotted on each graph. To facilitate this, y_data must be a 
        multi-level list with the following structure:

            y_data = [[["series name", AA1, AA2, ...], ["series name", AB1, AB2, ...]],
                        [["series name", BA1, BA2, ...], ["series name", BB1, BB2, ...]], 
                        ...]

        where datapoints labelled Axx are plotted in the top graph in the 
        window, and datapoints labelled AAx form a single line on the graph. The 
        data in each of the innermost lists forms a line, the lists of lists 
        form a graph, and the list of list of lists forms the whole window.

        Args:
            x_data (list[float]): data to plot on the horizontal axis.
            y_data (list[list[list[float]]]): data to plot on the vertical axis. 
            title (str, optional): main title for the graph. Defaults to "".

        Returns:
            int: signifies successful completion of the function.
        """
        
        number_of_subplots = len(y_data) # number of graphs within window
        
        for j in range(number_of_subplots): # iterate over number of graphs
            ax = plt.subplot(number_of_subplots, 1, j+1)
            
            for dataset in y_data[j]: # iterate over datasets within graph
                ax.plot(x_data[1:], dataset[1:], label=dataset[0])
                ax.set_xlim(xmin=0)
                ax.set_xlabel(x_data[0])
                plt.legend()

            plt.suptitle(title)

        plt.show()

        return 1

    

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
        columnData (list[]): can be used to store data for other methods, if 
            necessary
        
    Methods:
        __init__ : class constructor.
        file_path (property) : getter for the attribute of the same name.
        set_file_name : setter for attribute of the same name.
        ball_centred_velocities : calculates the velocities of the ball in 
            ball-centered coordinates.
        cartesian_positions : calculates the position of the ball in cartesian 
            coordinates.
        cartesian_velocities : calculates the velocities of the ball in 
            cartesian coordinates.
        delta_time : calculates the time step between each sample.
        smooth : runs the raw sensor data through a low pass filter to smooth 
            it.
        __integrate : does numerical integration on a dataset using the 
            trapezium rule.
        __pos_x : integrates velocity values (x) to get the spatial coordinate 
            in that direction.
        __pos_y : integrates velocity values (y) to get the spatial coordinate 
            in that direction.
        __pos_z : integrates velocity values (z) to get the spatial coordinate 
            in that direction.
        __vel_e_r : integrates acceleration values (e_r) to get the velocity in 
            that direction.
        __vel_e_theta : integrates acceleration values (e_theta) and (e_phi) to 
            get the velocity in the e_theta direction.
        __vel_e_phi : integrates acceleration values (e_theta) and (e_phi) to 
            get the velocity in the e_phi direction.
        __vel_x : returns list of velocity values in x direction.
        __vel_y : returns list of velocity values in y direction.
        __vel_z : returns list of velocity values in z direction.
    """

    def __init__(self, fileName=""):
        """Constructor for class.

        Args:
            fileName (str, optional): name of file to do calculations on. 
                Defaults to "".
        """
        self.fileName = fileName
        self.columnNumber = 1
        self.columnData = [] # empty for use as when needed
    
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


    def ball_centred_velocities(self, fileName=None, **kwargs):
        """Runs the separate operations that calculate the ball-centered 
        velocities.

        Sets the name of the file to operate on, and then checks to see if all 
        the columns that are required exist within the file, and if not, gets 
        them added. Then calls the individual methods to calculate each of the 
        velocities. Raises an exception to stop execution of 
        individual.add_column method with this method as an argument.

        Args:
            fileName (str, optional): name of the file to do calculations for.

        Raises:
            UniqueCaseException: raised to terminate execution of 
                individual.add_column method with this operation as an argument
        """

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)

        I = ProcessedData().individual
        I.set_file_name(fileName)

        # list of columns headers that need to be in the file already
        dependencies = {
            "delta time": self.delta_time,
            "acc (e_r)": self.smooth,
            "acc (e_theta)": self.smooth,
            "acc (e_phi)": self.smooth
        }

        # if dependency not in the file already, add them before calculating this column
        for key, value in dependencies.items():
            try:
                I.get_column_number(key)
            except ValueError:
                print("Column '{}' missing. Adding it to tracker file".format(key))
                I.add_column(value)

        # call functions to calculate each velocity
        I.add_column(self.__vel_e_r)
        I.add_column(self.__vel_e_theta)
        I.add_column(self.__vel_e_phi)

        raise UniqueCaseException

    def cartesian_positions(self, fileName=None, **kwargs):
        """Runs the separate operations that calculate the ball's coordinates in 
        Cartesian space.

        Sets the name of the file to operate on, and then checks to see if all 
        the columns that are required exist within the file, and if not, gets 
        them added. Then calls the individual methods to calculate each of the 
        velocities. Raises an exception to stop execution of 
        individual.add_column method with this method as an argument.

        Args:
            fileName (str, optional): name of the file to do calculations for.

        Raises:
            UniqueCaseException: raised to terminate execution of 
                individual.add_column method with this operation as an argument
        """

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)

        I = ProcessedData().individual
        I.set_file_name(fileName)

        # list of columns headers that need to be in the file already
        dependencies = {
            "delta time": self.delta_time,
            "vel (x)": self.cartesian_velocities,
            "vel (y)": self.cartesian_velocities,
            "vel (z)": self.cartesian_velocities
        }

        # if dependency not in the file already, add them before calculating this column
        for key, value in dependencies.items():
            try:
                I.get_column_number(key)
            except ValueError:
                print("Column '{}' missing. Adding it to tracker file".format(key))
                I.add_column(value)

        # call functions to calculate each velocity
        I.add_column(self.__pos_x)
        I.add_column(self.__pos_y)
        I.add_column(self.__pos_z)

        raise UniqueCaseException

    def cartesian_velocities(self, fileName=None, **kwargs):
        """Calculates and produces a list of velocities at each timestep in the 
        processed data file, and runs each of the separate operations that write 
        the data to the appropriate processed data file.
        
        Sets the name of the file to operate on, and then checks to see if all 
        the columns that are required exist within the file, and if not, gets 
        them added. Then calculates the values of the operation, and stores them 
        in a list. Then, calls the individual methods to calculate each of the 
        velocities. Raises an exception to stop execution of 
        individual.add_column method with this method as an argument. Note that 
        operations are all calculated in one go to reduce algorithmic 
        complexity.

        Args:
            fileName (str, optional): name of the file to do calculations for.

        Raises:
            UniqueCaseException: raised to terminate execution of 
                individual.add_column method with this operation as an argument
        """

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)

        I = ProcessedData().individual
        I.set_file_name(fileName)

        # list of columns headers that need to be in the file already
        dependencies = {
            "delta time": self.delta_time,
            "vel (e_r)": self.ball_centred_velocities,
            "vel (e_theta)": self.ball_centred_velocities,
            "vel (e_phi)": self.ball_centred_velocities,
            "euler (alpha)": self.ball_centred_velocities,
            "euler (beta)": self.ball_centred_velocities,
            "euler (gamma)": self.ball_centred_velocities
        }

        # if dependency not in the file already, add them before calculating this column
        for key, value in dependencies.items():
            try:
                I.get_column_number(key)
            except ValueError:
                print("Column '{}' missing. Adding it to tracker file".format(key))
                I.add_column(value)
        

        # column numbers of each column in processed data file
        columnNumbers = [I.get_column_number("delta time"),
                            I.get_column_number("vel (e_r)"),
                            I.get_column_number("vel (e_theta)"),
                            I.get_column_number("vel (e_phi)"),
                            I.get_column_number("euler (alpha)"),
                            I.get_column_number("euler (beta)"),
                            I.get_column_number("euler (gamma)")]
        
        # variables to store data
        timesteps = []
        velocities = np.zeros(3)
        angles = np.zeros(3)
        self.columnData = [[], [], []]

        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                next(f)
                
                for row in csv_file:
                    # store time, velocities and euler angles
                    timesteps.append(float(row[columnNumbers[0]]))
                    for i in range(0, 3):
                        velocities[i] = float(row[columnNumbers[i+1]])
                        angles[i] = float(row[columnNumbers[i+4]])

                    dcm = functions.generate_dcm(angles[0], angles[1], angles[2])
                    data = velocities.dot(dcm)
                    for i in range(0, 3):
                        self.columnData[i].append(data[i])
                    
        except FileNotFoundError:
            print("Couldn't open file:", fileName)

        I.add_column(self.__vel_x)
        I.add_column(self.__vel_y)
        I.add_column(self.__vel_z)

        self.columnData = [] # reset attribute to empty array

        raise UniqueCaseException

    def delta_time(self, fileName=None, heading=False):
        """Calculates the time step between consecutive samples of sensor data.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the values for this column are 
        calculated.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to actually calculate the value. Defaults to 
                False.

        Returns:
            list[float]: time steps between samples, maintaining the same 
                dimension as the input data.
        """

        if heading:
            return "delta time" # title of column in processed data file

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)
    
        data = []
        columnNumber = 0

        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                firstLine = f.readline()[:-1].split(",")
                data.append(firstLine[columnNumber])
                for row in csv_file:
                    data.append(float(row[columnNumber]))
        except FileNotFoundError:
            print("Couldn't open file:", fileName)
            return 0

        output = [0]
        for i in range(2, len(data)):
            output.append(data[i]-data[i-1])

        return output

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

        # make sure columnNumber is within range
        if self.columnNumber >= const.NUMBER_OF_COLUMNS:
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
            f = open(self.file_path)
        except FileNotFoundError:
            print("Couldn't open file:", fileName)
            return None

        csv_file = csv.reader(f)

        # skip header
        next(f)

        for row in csv_file:
            data.append(float(row[columnNumber]))
        f.close()

        self.columnNumber += 1 # increment

        # smooth data
        windowSize = 4
        smoothed = functions.moving_average(data, windowSize)       
        return [0] * (windowSize-1) + list(smoothed)


    def __integrate(self, data, timesteps, initialValue=0):
        """Calculates numerical integration for a given dataset using the 
        trapezium rule.

        Args:
            data (list[float]): data to be integrated.
            timesteps (list[int]): time between each sample of 'data'.
            initialValue (float, optional): initial offset for integration. 
                Defaults to 0.

        Returns:
            list[float]: integrated values
        """

        output = [initialValue]
        value = initialValue

        for i in range (1, len(timesteps)):
            value += (data[i-1] + data[i])/2 * timesteps[i]
            output.append(value)

        return output  
   
    def __pos_x(self, fileName=None, heading=False):
        """Calculates the x position (cartesian coordinates) at each sample of 
        sensor data.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the values for this column are 
        calculated.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to return the value. Defaults to False.

        Returns:
            list[float]: x position at each sample, maintaining the same 
                dimension as the input data.
        """

        if heading:
            return "pos (x)" # title of column in processed data file

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)

        I = ProcessedData().individual
        I.set_file_name(fileName)
        columnNumber_time = I.get_column_number("delta time")
        columnNumber = I.get_column_number("vel (x)")
        timesteps = []
        data = []

        # store file data in a list
        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                next(f)
                for row in csv_file:
                    timesteps.append(float(row[columnNumber_time]))
                    data.append(float(row[columnNumber]))
        except FileNotFoundError:
            print("Couldn't open file:", fileName)

        output = self.__integrate(data, timesteps) # integrate acceleration data
        return output
       
    def __pos_y(self, fileName=None, heading=False):
        """Calculates the y position (cartesian coordinates) at each sample of 
        sensor data.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the values for this column are 
        calculated.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to return the value. Defaults to False.

        Returns:
            list[float]: y position at each sample, maintaining the same 
                dimension as the input data.
        """

        if heading:
            return "pos (y)" # title of column in processed data file

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)

        I = ProcessedData().individual
        I.set_file_name(fileName)
        columnNumber_time = I.get_column_number("delta time")
        columnNumber = I.get_column_number("vel (y)")
        timesteps = []
        data = []

        # store file data in a list
        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                next(f)
                for row in csv_file:
                    timesteps.append(float(row[columnNumber_time]))
                    data.append(float(row[columnNumber]))
        except FileNotFoundError:
            print("Couldn't open file:", fileName)

        output = self.__integrate(data, timesteps) # integrate acceleration data
        return output
       
    def __pos_z(self, fileName=None, heading=False):
        """Calculates the z position (cartesian coordinates) at each sample of 
        sensor data.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the values for this column are 
        calculated.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to return the value. Defaults to False.

        Returns:
            list[float]: z position at each sample, maintaining the same 
                dimension as the input data.
        """

        if heading:
            return "pos (z)" # title of column in processed data file

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)

        I = ProcessedData().individual
        I.set_file_name(fileName)
        columnNumber_time = I.get_column_number("delta time")
        columnNumber = I.get_column_number("vel (z)")
        timesteps = []
        data = []

        # store file data in a list
        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                next(f)
                for row in csv_file:
                    timesteps.append(float(row[columnNumber_time]))
                    data.append(float(row[columnNumber]))
        except FileNotFoundError:
            print("Couldn't open file:", fileName)

        output = self.__integrate(data, timesteps) # integrate acceleration data
        return output
  
    def __vel_e_r(self, fileName=None, heading=False):
        """Calculates the e_r velocity (ball-centred coordinates) between 
        consecutive samples of sensor data.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the values for this column are 
        calculated.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to actually calculate the value. Defaults to 
                False.

        Returns:
            list[float]: e_r velocity at each sample, maintaining the same 
                dimension as the input data.
        """

        if heading:
            return "vel (e_r)" # title of column in processed data file

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)

        I = ProcessedData().individual
        I.set_file_name(fileName)
        columnNumber_time = I.get_column_number("delta time")
        columnNumber = I.get_column_number("acc (e_r)")
        timesteps = []
        data = []

        # store file data in a list
        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                next(f)
                for row in csv_file:
                    timesteps.append(float(row[columnNumber_time]))
                    data.append(float(row[columnNumber]))
        except FileNotFoundError:
            print("Couldn't open file:", fileName)

        output = self.__integrate(data, timesteps) # integrate acceleration data
        return output

    def __vel_e_theta(self, fileName=None, heading=False):
        """Calculates the e_theta velocity (ball-centred coordinates) between 
        consecutive samples of sensor data.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the values for this column are 
        calculated.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to actually calculate the value. Defaults to 
                False.

        Returns:
            list[float]: e_theta velocity at each sample, maintaining the same 
                dimension as the input data.
        """

        if heading:
            return "vel (e_theta)" # title of column in processed data file

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)

        I = ProcessedData().individual
        I.set_file_name(fileName)
        columnNumber_time = I.get_column_number("delta time")
        columnNumber = I.get_column_number("acc (e_theta)")
        timesteps = []
        data = []

        # store file data in a list
        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                next(f)
                for row in csv_file:
                    timesteps.append(float(row[columnNumber_time]))
                    data.append(float(row[columnNumber]))
        except FileNotFoundError:
            print("Couldn't open file:", fileName)

        output = self.__integrate(data, timesteps) # integrate acceleration data
        return output

    def __vel_e_phi(self, fileName=None, heading=False):
        """Calculates the e_phi velocity (ball-centred coordinates) between 
        consecutive samples of sensor data.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the values for this column are 
        calculated.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to actually calculate the value. Defaults to 
                False.

        Returns:
            list[float]: e_phi velocity at each sample, maintaining the same 
                dimension as the input data.
        """

        if heading:
            return "vel (e_phi)" # title of column in processed data file

        if fileName == None:
            fileName = self.fileName
        else:
            self.set_file_name(fileName)

        I = ProcessedData().individual
        I.set_file_name(fileName)
        columnNumber_time = I.get_column_number("delta time")
        columnNumber = I.get_column_number("acc (e_phi)")
        timesteps = []
        data = []

        # store file data in a list
        try:
            with open(self.file_path) as f:
                csv_file = csv.reader(f)
                next(f)
                for row in csv_file:
                    timesteps.append(float(row[columnNumber_time]))
                    data.append(float(row[columnNumber]))
        except FileNotFoundError:
            print("Couldn't open file:", fileName)

        output = self.__integrate(data, timesteps) # integrate acceleration data
        return output
   
    def __vel_x(self, fileName=None, heading=False):
        """Returns the x velocity (cartesian coordinates) between consecutive 
        samples of sensor data.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the precalculated values for this 
        column are returned.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to return the value. Defaults to False.

        Returns:
            list[float]: x velocity at each sample, maintaining the same 
                dimension as the input data.
        """

        if heading:
            return "vel (x)" # title of column in processed data file

        output = self.columnData[0]
        return output
    
    def __vel_y(self, fileName=None, heading=False):
        """Returns the y velocity (cartesian coordinates) between consecutive 
        samples of sensor data.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the precalculated values for this 
        column are returned.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to return the value. Defaults to False.

        Returns:
            list[float]: y velocity at each sample, maintaining the same 
                dimension as the input data.
        """

        if heading:
            return "vel (y)" # title of column in processed data file

        output = self.columnData[1]
        return output
    
    def __vel_z(self, fileName=None, heading=False):
        """Returns the z velocity (cartesian coordinates) between consecutive 
        samples of sensor data.

        If the 'heading' parameter is 'True', the method simply returns the 
        heading for this column. Otherwise, the precalculated values for this 
        column are returned.

        Args:
            fileName (str): name of the file to do calculations for.
            heading (bool): set this to 'True' if only the heading title is 
                wanted. Set 'False' to return the value. Defaults to False.

        Returns:
            list[float]: z velocity at each sample, maintaining the same 
                dimension as the input data.
        """

        if heading:
            return "vel (z)" # title of column in processed data file

        output = self.columnData[2]
        return output
   

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
                time = float(row[0])
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
