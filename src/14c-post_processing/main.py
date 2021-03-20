from obj import const
from obj import global_tracker
from obj import functions
from obj import processed_data
from obj import raw_data

def get_prompt(level):
    """Prints out the current level of menu and receives user input about their 
    selection.

    Args:
        level (str): Current menu level.

    Returns:
        str: the new level based on the current level and the user's input.
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
    elif level == "1e":
        options = level1e
    elif level == "1ea":
        options = level1ea
    elif level == "1eb":
        options = level1eb
    
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
        keys (list[str]): available input options.

    Returns:
        str: user's input.
    """

    while True:
        choice = input("\nEnter your choice: ").lower()
        if choice in keys:
            return choice
        else:
            print("Invalid input")

def sanitise_file_name(addDataDirectory=False):
    """Gets user to input name of a file, then removes whitespace and corrects 
    upper/lower cases in the file name.

    Returns:
        str: sanitised file name.
    """

    print("Enter file name (in format '{}')".format(const.RAW_DATA_TITLE_FORMAT + 
                                                        const.RAW_DATA_FILE_TYPE))
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
        level (str): the current level of menu to print.
        menu (dict): the menu at the current level.
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

# 1ba
def set_parameters_health(overwrite=True, showWarnings=True):
    """Allows the user to set parameters to initialise the 'RawData.health' 
    object.

    Args:
        overwrite (bool, optional): value for class. Defaults to True.
        showWarnings (bool, optional): value for class. Defaults to True.

    Returns:
        bool: value of overwrite.
        bool: value of showWarnings.
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
    
# 1ca
def set_parameters_processed(overwrite=False):
    """Allows the user to set parameters to initialise the 'P.health' 
    object.

    Args:
        overwrite (bool, optional): value for class. Defaults to True.
        showWarnings (bool, optional): value for class. Defaults to True.

    Returns:
        bool: value of overwrite.
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

    print("Parameters chosen:")
    print("  - overwrite = {}".format(overwrite))

    return overwrite

# 1eab
def set_parameters_graph_sensor_data(filtered=True, unfiltered=False):
    """Allows the user to set parameters to run the 
    '_individual.graph_sensor_data' method.

    Args:
        filtered (bool, optional): value for method. Defaults to True.
        unfiltered (bool, optional): value for method. Defaults to False.

    Returns:
        bool: value of filteredwrite.
        bool: value of unfiltered.
    """
    
    # set possible values for overwrite
    options = {
        "0": False,
        "1": True
    }

    print("Set 'filtered' (default is '{}')".format(filtered))
    for (key, val) in options.items():
        print(str(key) + ") " + str(val))
    
    while True:
        choice = input().lower()
        if choice == "": # if blank, don't change value
            break
        elif choice in options.keys():
            filtered = options[choice]
            break
        else:
            print("Invalid input")

    # options don't change for 'unfiltered

    print("Set 'unfiltered' (default is '{}')".format(unfiltered))
    for (key, val) in options.items():
        print(str(key) + ") " + str(val))
    
    while True:
        choice = input().lower()
        if choice == "": # if blank, don't overwrite value
            break
        elif choice in options.keys():
            unfiltered = options[choice]
            break
        else:
            print("Invalid input")

    print("Parameters chosen:")
    print("  - filtered = {}".format(filtered))
    print("  - unfiltered = {}".format(unfiltered))

    return filtered, unfiltered
    

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
            # update class attributes
            H.overWrite = overwrite
            H.showWarnings = showWarnings
            level = level[:-1]
        elif level == "1bb": # assess all files
            if H.check_all_files():
                print("Recommended to create processed data files. Create? (y/n)")
                if input() == "y":
                    level = "1c"
                    continue
            level = level[:-1]
        elif level == "1bc": # assess a specific file
            fileName = sanitise_file_name(True)
            if H.check_one_file(fileName) >= const.passedWithWarnings:
                print("Recommended to create processed data file. Create? (y/n)")
                if input() == "y":
                    level = "1c"
                    continue
            level = level[:-1]
        elif level == "1c": # processed files
            print("Set parameters:") # set parameters before creating objects
            overwrite = set_parameters_processed()
            P = processed_data.ProcessedData(overwrite)
        elif level == "1ca": # set parameters
            print("Set parameters:") # set parameters before creating objects
            overwrite = set_parameters_processed(overwrite)
            # update class attributes
            P.overwrite = overwrite
            level = level[:-1]
        elif level == "1cb": # create processed data files for all raw data files
            if P.create_all_processed_data_files():
                print("Completed successfully")
                print("Recommended to run operations (e.g. smooth sensor readings). Do it? (y/n)")
                if input() == "y":
                    level = "1cd"
                    continue
            level = level[:-1]
        elif level == "1cc": # create a processed data file for a specific raw data file
            fileName = sanitise_file_name(False)
            newFile = P.create_single_processed_data_file(functions.add_data_directory(fileName))
            if newFile:
                print("Added file " + newFile)
                print("Recommended to run operations (e.g. smooth sensor readings). Do it? (y/n)")
                if input() == "y":
                    level = "1cd"
                    continue
            else:
                print("File {} could not be added".format(fileName))
            level = level[:-1]
        elif level == "1cd": # calculate an operation for all files
            I = P.individual
            print("Enter name of calculation, or 'q' to quit")
            for key in calculations.keys():
                print(" -", key)

            column_header = get_input(calculations.keys())
            if column_header == "q":
                pass
            elif column_header == "all":
                for entry in P.get_all_processed_files():
                    I.set_file_name(entry)
                    print("File: " + entry)
                    for key in calculations.keys():
                        if key == "all" or key == "q":
                            continue
                        print("  Calculating '{}'...".format(key))
                        I.add_column(calculations[key])
            else:
                print("  Calculating '{}'...".format(column_header))
                for entry in P.get_all_processed_files():
                    I.set_file_name(entry)
                    print("File: " + entry)
                    I.add_column(calculations[column_header])
            level = level[:-1]
        elif level == "1d": # tracker
            G = global_tracker.GlobalFile(True)
        elif level == "1da": # add raw data file to tracker
            fileName = sanitise_file_name(True)
            if G.add_file(fileName):
                print("File added to tracker successfully")
            else:
                print("File not added to tracker")
            level = level[:-2]
        elif level == "1db": # check if a raw data file has been listed in tracker
            fileName = sanitise_file_name(True)
            if G.is_file_recorded(fileName):
                print("File ({}) is listed in tracker".format(fileName))
            else:
                print("File ({}) is not listed in tracker".format(fileName))
            level = level[:-1]
        elif level == "1dc": # remove deleted files from tracker
            G.remove_deleted()
            level = level[:-1]
        elif level == "1dd": # add/update a metric to tracker
            # print menu and store user's input
            print("Enter name of metric, or 'q' to quit")
            for key in metrics.keys():
                print(" -", key)

            column_header = get_input(metrics.keys())
            if column_header == "q":
                pass
            elif column_header == "all":
                for key in metrics.keys():
                    if key == "all" or key == "q":
                        continue
                    print("Calculating '{}'...".format(key))
                    G.add_metric(metrics[key])
            else:
                G.add_metric(metrics[column_header])
            
            level = level[:-1]
        elif level == "1de": # remove a metric from the tracker
            # print menu and store user's input
            print("Enter name of metric, or 'q' to quit")
            for key in metrics.keys():
                print(" -", key)

            column_header = get_input(metrics.keys())
            if column_header == "q":
                pass
            elif column_header == "all":
                for key in metrics.keys():
                    if key == "all" or key == "q":
                        continue
                    if G.remove_metric(key):
                        print("Removed column '{}'".format(key))
            else:
                if G.remove_metric(column_header):
                    print("Removed column '{}'".format(column_header))
            level = level[:-1]
        elif level == "1e": # analysis
            filtered = True
            unfiltered = False
        elif level == "1ea": # individual file analysis
            print("Set parameters:")
            fileName = functions.raw_to_processed(sanitise_file_name(True))
            P = processed_data.ProcessedData()
            I = P.individual
            I.set_file_name(fileName)

            healthStatus = I.get_health_status()

            if healthStatus >= const.passedWithWarnings:
                print("File selected: ", fileName)
            elif healthStatus == -1:
                print("File not found, choose another file or run a different operation.")
                level = level[:-1]
            else:
                print("File {} not marked as healthy, choose another or check the file first."
                        .format(fileName))
                level = level[:-1]
        elif level == "1eaa": # update parameters
            fileName = functions.raw_to_processed(sanitise_file_name(True))

            I.set_file_name(fileName)

            if I.get_health_status() >= const.passedWithWarnings:
                print("File selected: ", fileName)
                level = level[:-1]
            else:
                print("File {} not marked as healthy, choose another or check the file first."
                        .format(fileName))
                level = level[:-2]
        elif level == "1eab": # graph of raw sensor values
            print("Set parameters:") # set parameters before creating objects
            filtered, unfiltered = set_parameters_graph_sensor_data(filtered=filtered, 
                                                                    unfiltered=unfiltered)
            I.graph_sensor_data(filtered=filtered, unfiltered=unfiltered)
            level = level[:-1]
        elif level == "1eac": # graph flight path
            I.graph_flight_path()
            level = level[:-1]
        elif level == "1eb": # population analysis
            G = global_tracker.GlobalFile(True)

        print("\n")
        level = get_prompt(level)
        
        if level == "1": # when return to the main menu
            # delete any open objects
            try: del G
            except: pass
            try: del H
            except: pass
            try: del I
            except: pass
            try: del P
            except: pass
            try: del R
            except: pass
        elif level == "": # quit
            break


# menus
level1 = {
    "a": "View architecture of interface",
    "b": "Health check",
    "c": "Processed files",
    "d": "Tracker",
    "e": "Analysis",
    "q": "Quit program"
}

level1b = {
    "a": "Change parameters",
    "b": "Assess all files",
    "c": "Assess a specific file",
    "q": "Quit 'Health check'"
}

level1c = {
    "a": "Change parameters",
    "b": "Create processed data files for all raw data files",
    "c": "Create a processed data file for a specific raw data file",
    "d": "Add/update an operation for all files",
    "q": "Quit 'Processed files'"
}

level1d = {
    "a": "Add raw data file to tracker",
    "b": "Check if a raw data file has been listed in tracker",
    "c": "Remove deleted files from tracker",
    "d": "Add/update a metric in tracker",
    "e": "Remove a metric from the tracker",
    "q": "Quit 'Tracker'"
}

level1e = {
    "a": "Individual file analysis",
    "b": "Population analysis",
    "q": "Quit 'Analysis'"
}

level1ea = {
    "a": "Update parameters",
    "b": "Graph of raw sensor values",
    "c": "Graph flight path",
    "q": "Quit 'Individual file analysis'"
}

level1eb = {
    "a": "*Graph metrics against each other",
    "q": "Quit 'Population analysis'"
}


# calculations
calculations = {
    "all": None,
    "smooth": processed_data.ProcessedData().individual.calculations.smooth,
    "ball centred velocities": processed_data.ProcessedData().individual.calculations.ball_centred_velocities,
    "cartesian velocities": processed_data.ProcessedData().individual.calculations.cartesian_velocities,
    "cartesian positions": processed_data.ProcessedData().individual.calculations.cartesian_positions,
    "q": None
}

# metric
metrics = {
    "all": None,
    "time of throw": processed_data.ProcessedData().metrics.total_time,
    "spiral rate": processed_data.ProcessedData().metrics.spiral_rate,
    "q": None
}


if __name__ == "__main__":
    main()