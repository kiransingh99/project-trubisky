from obj import functions
from obj import global_tracker
from obj import raw_data

def main():
    print("\n\n")
    R = raw_data.RawData(overwrite=True, showWarnings=False)
    # R.health.check_all_files()
    # R.individual

    G = global_tracker.GlobalFile()
    G.remove_deleted()

    O = R.individual.operations
    # G.populate_metric(O.total_time)



if __name__ == "__main__":
    main()