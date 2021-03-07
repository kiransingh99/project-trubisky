from . import const
import os.path
import csv


class ProcessedData: # DOCSTRING
    
    def __init__(self, overwrite): # COMPLETE, DOCSTRING
        self.overwrite = overwrite
        
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

    
    def create_all_processed_data_files(self): # DOCSTRING
        for entry in os.listdir(self.DATA_DIRECTORY):
            rawFilePath = os.path.join(self.DATA_DIRECTORY, entry)
            rawFileName = rawFilePath[const.PATH_LENGTH_TO_DATA_DIR:]

            # only check raw data files saved as a csv 
            if entry[:len(const.RAW_DATA_PREFIX)] == const.RAW_DATA_PREFIX:
                 if entry.endswith(".csv"): # only check CSV files

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

        return processedFileName
        

