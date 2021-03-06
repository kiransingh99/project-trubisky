from obj import const
from obj import global_tracker
from obj import functions
from obj import raw_data

def get_prompt(level):
    """Prints out the current level of menu and receives user input about their 
    selection.

    Args:
        level (str): Current menu level

    Returns:
        str: the new level based on the current level and the user's input
    """

    options = {} # empty dictionary

    # decide which menu to print
    if level == "1":
        print("Main menu:\n")
        options = level1
    elif level == "1b":
        options = level1b
    elif level == "1c":
        options = level1c
    elif level == "1d":
        options = level1d
    elif level == "1da":
        options = level1da
    elif level == "1db":
        options = level1db
    
    # print menu and store user's input
    for (key, val) in options.items():
        print(key + ") " + val)

    option = get_input(options.keys())

    if option.lower() == "q": # quit goes up a level
        newLevel = level[:-1]
    else:
        newLevel = level + option #append user input to current level to generate new level

    return newLevel

def get_input(keys):
    """Gets a user input to choose the next level and verifies that it is a 
    valid option.

    Args:
        keys (list[str]): available input options

    Returns:
        str: user's input
    """

    while True:
        choice = input("\nEnter your choice: ").lower()
        if choice in keys:
            return choice
        else:
            print("Invalid input")

def sanitise_file_name(addDataDirectory = False):
    """Gets user to input name of a file, then removes whitespace and corrects 
    upper/lower cases in the file name.

    Returns:
        str: sanitised file name
    """
    print("Enter file name (in format '{}')".format(const.RAW_DATA_TITLE_FORMAT))
    # remove white space and everything before the last "\"
    userinput = input().strip().split(sep="\\")[-1] 

    # remove file extension if already included, and add it (back) on in lower case
    if userinput[-len(const.RAW_DATA_FILE_TYPE):].lower() == const.RAW_DATA_FILE_TYPE:
        fileName = userinput[:-len(const.RAW_DATA_FILE_TYPE)].upper() + const.RAW_DATA_FILE_TYPE
    else:
        fileName = userinput.upper() + const.RAW_DATA_FILE_TYPE
    
    # add parent folder 
    if addDataDirectory:
        fileName = functions.add_data_directory(fileName)
    
    return fileName

#1a
def print_architecture(level, menu):
    """Prints architecture of the entire menu at all levels.

    Args:
        level (str): the current level of menu to print
        menu (dict): the menu at the current level
    """

    for (key, val) in menu.items():
        
        print("".join("  " for character in level), end="") # indent for lower levels
        print(key + ") " + val) # print menu options
        
        # if any options have submenus, print them too
        if level == "1":
            if key == "b":
                print_architecture("1b", level1b)
            elif key == "c":
                print_architecture("1c", level1c)
            elif key == "d":
                print_architecture("1d", level1d)
        elif level == "1d":
            if key == "a":
                print_architecture("1ea", level1b)
            elif key == "b":
                print_architecture("1eb", level1c)

#1ba
def set_parameters_health(overwrite = True, showWarnings = True):
    """Allows the user to set parameters to initialise the 'RawData.health' 
    object.

    Args:
        overwrite (bool, optional): value for class. Defaults to True.
        showWarnings (bool, optional): value for class. Defaults to True.

    Returns:
        bool: value of overwrite
        bool: value of showWarnings
    """
    
    # set possible values for overwrite
    options = {
        "0": False,
        "1": True
    }

    print("Set 'overwrite' (default is '{}')".format(overwrite))
    for (key, val) in options.items():
        print(str(key) + ") " + str(val))
    
    while True:
        choice = input().lower()
        if choice == "": # if blank, don't change value
            break
        elif choice in options.keys():
            overwrite = options[choice]
            break
        else:
            print("Invalid input")

    # options don't change for 'showWarnings

    print("Set 'showWarnings' (default is '{}')".format(showWarnings))
    for (key, val) in options.items():
        print(str(key) + ") " + str(val))
    
    while True:
        choice = input().lower()
        if choice == "": # if blank, don't overwrite value
            break
        elif choice in options.keys():
            showWarnings = options[choice]
            break
        else:
            print("Invalid input")

    print("Parameters chosen:")
    print("  - overwrite = {}".format(overwrite))
    print("  - showWarnings = {}".format(showWarnings))

    return overwrite, showWarnings
    

def main():
    print("\n\n")
    level = "1"

    while True:
        
        if level == "1a": # print architecture
            print_architecture("1", level1)
            level = level[:-1] # remove last character of 'level' when task complete
            print("\n\n")
        elif level == "1b": # health
            print("Set parameters:") # set parameters before creating objects
            overwrite, showWarnings = set_parameters_health()
            R = raw_data.RawData(overwrite, showWarnings)
            H = R.health
        elif level == "1ba": # set parameters
            overwrite, showWarnings = set_parameters_health(overwrite, showWarnings)
            # update class attributes instead of recreating object
            H.overWrite = overwrite
            H.showWarnings = showWarnings
            level = level[:-1]
        elif level == "1bb": # assess all files
            H.check_all_files()
            level = level[:-1]
        elif level == "1bc": # assess a specific file
            fileName = sanitise_file_name(False)
            filePath = const.DATA_DIRECTORY + fileName
            H.check_one_file(filePath)
            level = level[:-1]
        elif level == "1c": # tracker
            G = global_tracker.GlobalFile(True)
        elif level == "1ca": # add raw data file to tracker
            fileName = sanitise_file_name(True)
            if G.add_file(filePath):
                print("File added to tracker successfully")
            else:
                print("File not added to tracker")
            level = level[:-1]
        elif level == "1cb": # check if a raw data file has been listed in tracker
            fileName = sanitise_file_name(True)
            if G.is_file_recorded(filePath):
                print("File ({}) is listed in tracker".format(filePath))
            else:
                print("File ({}) is not listed in tracker".format(filePath))
            level = level[:-1]
        elif level == "1cc": # remove deleted files from tracker
            G.remove_deleted()
            level = level[:-1]
        elif level == "1cd": # add/update a metric to tracker
            # print menu and store user's input
            print("Enter name of operation, or 'q' to quit")
            for key in operation.keys():
                print(" -", key)

            column_header = get_input(operation.keys())
            if column_header == "q":
                pass
            elif column_header == "all":
                for key in operation.keys():
                    if key == "all" or key == "q":
                        continue
                    print("Calculating '{}'...".format(key))
                    G.add_metric(operation[key])
            else:
                G.add_metric(operation[column_header])
            
            level = level[:-1]
        elif level == "1ce": # remove a metric from the tracker
            # print menu and store user's input
            print("Enter name of operation, or 'q' to quit")
            for key in operation.keys():
                print(" -", key)

            column_header = get_input(operation.keys())
            if column_header == "q":
                pass
            elif column_header == "all":
                for key in operation.keys():
                    if key == "all" or key == "q":
                        continue
                    try:
                        columnNumber = G.get_column_number(key)
                    except ValueError as e: # if column not found
                        print(e)
                    else:
                        G.remove_metric(columnNumber)
            else:
                try:
                    columnNumber = G.get_column_number(column_header)
                except ValueError as e: # if column not found
                    print(e)
                else:
                    G.remove_metric(columnNumber)
            level = level[:-1]
        elif level == "1d": # analysis
            n = 6 # number of subplots
        elif level == "1da": # individual file analysis
            print("Set parameters:")
            fileName = sanitise_file_name(True)
            R = raw_data.RawData(fileName = fileName)
            I = R.individual

            healthStatus = I.get_health_status()

            if healthStatus >= const.passedWithWarnings:
                print("File selected: ", fileName)
            elif healthStatus == -1:
                continue
            else:
                print("File {} not marked as healthy, choose another or check the file first."
                        .format(fileName))
                level = level[:-1]
        elif level == "1daa": # update parameters
            fileName = sanitise_file_name(True)

            I.set_file_name(fileName)

            if I.get_health_status() >= const.passedWithWarnings:
                print("File selected: ", fileName)
            else:
                print("File {} not marked as healthy, choose another or check the file first."
                        .format(fileName))
            level = level[:-1]
        elif level == "1dab": # graph of raw sensor values
            n_str = input("How many subplots? Default is {} ".format(n))
            if n_str == "":
                pass
            elif functions.isFloat(n_str):
                n = int(n_str)
            else:
                print("Invalid input, using {} subplots".format(n))
            I.graph_sensor_data(n)
            level = level[:-1]
        elif level == "1dac": # graph flight path
            I.graph_flight_path()
            level = level[:-1]
        elif level == "1db": # population analysis
            G = global_tracker.GlobalFile(True)

        print("\n\n")
        level = get_prompt(level)
        
        if level == "1": # when return to the main menu
            # delete any open objects
            try: del G
            except: pass
            try: del H
            except: pass
            try: del I
            except: pass
            try: del R
            except: pass
        elif level == "": # quit
            break


# operations
operation = {
    "all": None,
    "time of throw": raw_data.RawData().individual.operations.total_time,
    "q": None
}

# menus
level1 = {
    "a": "View architecture of interface",
    "b": "Health check",
    "c": "Tracker",
    "d": "Analysis",
    "q": "Quit program"
}

level1b = {
    "a": "Change parameters",
    "b": "Assess all files",
    "c": "Assess a specific file",
    "q": "Quit 'Health check'"
}

level1c = {
    "a": "Add raw data file to tracker",
    "b": "Check if a raw data file has been listed in tracker",
    "c": "Remove deleted files from tracker",
    "d": "Add/update a metric in tracker",
    "e": "Remove a metric from the tracker",
    "q": "Quit 'Tracker'"
}

level1d = {
    "a": "Individual file analysis",
    "b": "Population analysis",
    "q": "Quit 'Analysis'"
}

level1da = {
    "a": "Update parameters",
    "b": "Graph of raw sensor values",
    "c": "Graph flight path",
    "q": "Quit 'Individual file analysis'"
}

level1db = {
    "a": "*Graph metrics against each other",
    "q": "Quit 'Population analysis'"
}

if __name__ == "__main__":
    main()