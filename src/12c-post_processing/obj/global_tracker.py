class GlobalFile:
    #handles everything to do with the global file
    def __init__(self, globalTracker):
        __globalFile = globalTracker

    @property
    def globalFile(self):
        return self.__globalFile

    def add_files(self, file):
        #add metrics from untracked files to global tracker file and mark health
        #as 'True'
        pass

    def add_metric(self, file):
        #add another column to global tracker
        pass
    
    def write_to_file(self, file, metric, data):
        #write given data to tracker file, with the row and column given by
        #'file' and 'metric' respectively

    def check_file_exists(self, file):
        #check if filename recorded in tracker exists 
        pass