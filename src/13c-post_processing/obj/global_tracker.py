class GlobalFile:
    #handles everything to do with the global file
    def __init__(self, globalTracker):
        self.__globalFile = globalTracker

    def __del__(self):
        print("GlobalFile object destroyed")

    @property
    def globalFile(self):
        return self.__globalFile

    def add_file(self, fileName):
        #check if file is already listed. If it is, return false, if not, aadd
        #metrics from untracked files to global tracker file and mark health
        #as 'False' (and return True)
        pass

    def mark_file_as_healthy(self, fileName):
        #find given file in the document and mark it as healthy if it is not
        #already. Return True if completed, return False if no change mad
        pass

    def add_metric(self, file):
        #add another column to global tracker
        pass
    
    def write_to_file(self, file, metric, data):
        #write given data to tracker file, with the row and column given by
        #'file' and 'metric' respectively
        pass

    def check_file_exists(self, file):
        #check if filename recorded in tracker exists 
        pass