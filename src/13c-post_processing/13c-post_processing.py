#from obj import global_tracker
from obj import functions
from obj import raw_data

def main():
    R = raw_data.RawData(overwrite=True, showWarnings=False)
    R.health.check_all_files()
    #R.individual



if __name__ == "__main__":
    print("\n\n")
    main()