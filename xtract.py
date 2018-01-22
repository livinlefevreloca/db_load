#!Python3
#extract_funcs.py -  module for functions used to extract data from csv files

import os, shutil
from zipfile import ZipFile

def extract_files(zip_file, root, extract_too):
    END_DIR = os.path.join(os.getcwd(), os.path.join(extract_too, ''.join(list(zip_file)[:-4])))
    print(END_DIR)
    try:
        os.mkdir(os.path.join(os.getcwd(), extract_too))
    except OSError:
        print("Directory %s already exists" %(extract_too))
    current_zf = os.path.join(root,zip_file);
    ZipFile(current_zf).extractall(END_DIR)
    
def walk_folder(to_walk):
    WALK_DIR = os.path.join(os.getcwd(), to_walk)
    for root, dirs, files in os.walk(WALK_DIR):
        for file in files:
            extract_files(file,root,'data')    
        
    shutil.rmtree(to_walk)    



