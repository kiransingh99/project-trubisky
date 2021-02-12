from obj import raw_data
from obj import global_tracker


def main():
    R = raw_data.RawData()
    R.check_health_all_files()



if __name__ == "__main__":
    print("\n\n")
    main()