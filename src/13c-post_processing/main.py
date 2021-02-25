from obj import const
from obj import global_tracker
from obj import functions
from obj import raw_data

def get_prompt(level):
    options = {}

    print()

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
    
    for (key, val) in options.items():
        print(key + ") " + val)

    option = get_input(options.keys)

    if option.lower() == "q":
        newLevel = level[:-1]
    else:
        newLevel = level + option

    return newLevel

def get_input(keys):
    while True:
        choice = input("\nEnter your choice: ").lower()
        if choice in keys():
            return choice
        else:
            print("Invalid input")

#1a
def print_architecture(level, menu):
    for (key, val) in menu.items():
        
        print("".join("  " for character in level), end="")
        
        print(key + ") " + val)
        
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
    
    options = {
        "0": False,
        "1": True
    }

    print("Set 'overwrite' (default is '{}')".format(overwrite))
    for (key, val) in options.items():
        print(str(key) + ") " + str(val))
    
    while True:
        choice = input()
        if choice == "":
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
        choice = input()
        if choice == "":
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
        print()
        level = get_prompt(level)
        
        if level == "1a": # print architecture
            print_architecture("1", level1)
            level = level[:-1]
            print("\n\n")
        elif level == "1b": # health
            print("Set parameters:")
            overwrite, showWarnings = set_parameters_health()
            R = raw_data.RawData(overwrite, showWarnings)
            H = R.health
        elif level == "1ba": # set parameters
            overwrite, showWarnings = set_parameters_health(overwrite, showWarnings)
            R.overWrite = overwrite
            H.overWrite = overwrite
            R.showWarnings = showWarnings
            H.showWarnings = showWarnings
            level = level[:-1]
        elif level == "1bb": # assess all files
            H.check_all_files()
            level = level[:-1]
        elif level == "1bc": # assess a specific file
            fileName = input("Enter file name (in format 'RAW-yyyy.mm.dd-hh.mm.ss.csv')")
            filePath = const.DATA_DIRECTORY + fileName
            H.check_one_file(filePath)
            level = level[:-1]

        
        if level == "1":
            try: del R
            except: pass
            try: del H
            except: pass
        elif level == "":
            break
        
    


level1 = {
    "a": "View architecture of interface",
    "b": "Health check",
    "c": "*Tracker",
    "d": "*Analysis",
    "q": "Quit program"
}

level1b = {
    "a": "Change parameters",
    "b": "Assess all files",
    "c": "Assess a specific file",
    "q": "Quit 'Health check'"
}

level1c = {
    "a": "*Add raw data file to tracker",
    "b": "*Check if a raw data file has been listed in tracker",
    "c": "*Remove file from tracker",
    "d": "*Add a metric to tracker",
    "e": "*Update/populate a metric",
    "f": "*Remove a metric from the tracker",
    "q": "Quit 'Tracker'"
}

level1d = {
    "a": "*Individual file analysis",
    "b": "*Population analysis",
    "q": "Quit 'Analysis'"
}

level1da = {
    "a": "*Graph of raw sensor values",
    "b": "*Graph flight path",
    "q": "Quit 'Individual file analysis'"
}

level1db = {
    "a": "*Graph metrics against each other",
    "q": "Quit 'Population analysis'"
}

if __name__ == "__main__":
    main()