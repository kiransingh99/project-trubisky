from . import const
from . import functions
from . import global_tracker
import csv
import inspect
import matplotlib.pyplot as plt
import os.path


class ProcessedData: # DOCSTRING
    
    def __init__(self, overwrite=False, fileName=""): # COMPLETE, DOCSTRING
        self.overwrite = overwrite
        self.fileName = fileName
        
    def __del__(self):
        """Destructor for class.
        """

        # print("ProcessedData object destroyed")
        pass

    @property
    def DATA_DIRECTORY(self):
        """Getter for constant of the same name.

        Returns:
            str: the path to the directory that stores the data files
        """
        
        return const.DATA_DIRECTORY

    @property
    def individual(self): #DOCSTRING
        return _SingleFile(self.fileName)

    @property
    def ensemble(self, fileName=""): # DOCSTRING
        """Creates instance of _MetricCalculator as an object of 
        _SingleRawDataFile.

        Creates an instance of the '_MetricCalculator' class as an object 
        called 'self.operations', where 'self' is the name of the instance of 
        '_SingleRawDataFile'.

        Args:
            fileName (str, optional): name of the file to operate on. None that 
                this must be passed to the operations sub-method at some point. 
                Defaults to "".

        Returns:
            _Ensemble object: instance of class
        """

        return _Ensemble(fileName)


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

        rawFilePath = const.DATA_DIRECTORY + "\\" + rawFileName[const.LENGTH_OF_DATA_DIR:]
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
        




class _SingleFile:
    """Handler for processing of individual processed data files.

    Attributes:
        fileName (str) : name of the file to calculate the metric for
        filePath (str) : file path to the file which will be operated on

    Methods:
        __init__ : constructor for class
        operations : {property) groups the methods that calculate 
            metrics for the global tracker
        file_path : (property) getter for the attribute of the same name
        set_file_name : setter for the attribute of the same name
        get_health_status : checks if a file has been marked as healthy in the 
            tracker
        graph_sensor_data : creates a graph of the raw sensor data over time
        graph_flight_path : DOCSTRING
    """

    def __init__(self, fileName):
        """[summary]

        Args:
            fileName ([type]): [description]
        """
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

    @property
    def operations(self, fileName=""):
        """Creates instance of _MetricCalculator as an object of 
        _SingleRawDataFile.

        Creates an instance of the '_MetricCalculator' class as an object 
        called 'self.operations', where 'self' is the name of the instance of 
        '_SingleRawDataFile'.

        Args:
            fileName (str, optional): name of the file to operate on. None that 
                this must be passed to the operations sub-method at some point. 
                Defaults to "".

        Returns:
            _MetricCalculator object: instance of class
        """

        return _MetricCalculator(fileName)

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

    def graph_raw_sensor_data(self): # DOCSTRING
        """Creates a graph of the raw sensor data over time.

        First, checks the raw data file has passed its health checks. Then 
        stores the data in each of the columns in its own list, which is used 
        to generate a graph of all the values together.

        Returns:
            int: signifies successful completion of the method
        """

        G = global_tracker.GlobalFile(False)
        healthStatus = G.get_health_status(self.raw_file_name)
        del G

        filePath = self.file_path

        if healthStatus == -1: # not in file
            print("File not found")
            return 0
        elif healthStatus <= const.failed: # failed or untested
            print("File has not been marked as healthy")
            return 0
        else: # healthy
            with open(filePath) as f:
                raw_data = csv.reader(f)
                data = []

                # create blank list of lists to store data
                for i in range(0, const.NUMBER_OF_COLUMNS):
                    data.append([])

                next(f)

                for row in raw_data:
                    for i, entry in enumerate(row):
                        data[i].append(float(entry))

            time = data[0]

            #plot linear acceleration and angular velocity separately
            fig, (linAcc, angVel, eulerAng) = plt.subplots(3, sharex=True)
            for i in range(1, len(data)):
                if i < 4:
                    linAcc.plot(time, data[i], label=const.COLUMN_HEADERS[i])
                elif i < 7:
                    angVel.plot(time, data[i], label=const.COLUMN_HEADERS[i])
                elif i < 10:
                    eulerAng.plot(time, data[i], label=const.COLUMN_HEADERS[i])
            
            fig.suptitle("Raw Sensor Data against Time")
            linAcc.legend()
            angVel.legend()
            eulerAng.legend()
            fig.show()           

            return 1

    def graph_flight_path(self): #COMPLETE, DOCSTRING
        print("TO DO THIS FUNCTION STILL")

    def total_time(self, fileName = None, heading=False):
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




class _MetricCalculator:
    """Object that calculates all the metrics.

    Attributes:
        fileName (str) : name of the file to calculate the metric for
        filePath (str) : file path to the file which will be operated on

    Methods:
        __init__ : constructor for class
        file_path : (property) getter for the attribute of the same name
        set_file_name : setter for the attribute of the same name
        all : runs all methods in this class that calculate a metric
        total_time : metric calculator for the time of the throw recorded
    """

    def __init__(self, fileName):
        """Constructor for class. Sets class attribute.

        Args:
            fileName (str): the name of the file to calculate a metric for
        """
        
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



class _Ensemble:
    """Object that calculates all the metrics.

    Attributes:
        fileName (str) : name of the file to calculate the metric for
        filePath (str) : file path to the file which will be operated on

    Methods:
        __init__ : constructor for class
        file_path : (property) getter for the attribute of the same name
        set_file_name : setter for the attribute of the same name
        all : runs all methods in this class that calculate a metric
        total_time : metric calculator for the time of the throw recorded
    """

    def __init__(self, fileName):
        pass