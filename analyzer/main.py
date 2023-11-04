from ProjectManager import *
from ByteCode import *

if __name__ == "__main__":

    if not Manager.check_if_dir_exists():
        print("Init")
        Manager.init_test_data()
    
    mod_files = Manager.findModifiedFiles()
    for file in mod_files :
        name = os.path.basename(file)
        Manager.getDiff(file, name)