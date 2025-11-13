from file_sorter import *

def main():
    folder_path = input("Enter path: ")
    sort(folder_path)
    make_folder()
    move_files()

if __name__ == "__main__":
    main()