import os
import shutil

file_dict = {}
file_list = []

def sort(folder_path):
    items = os.listdir(folder_path)
    
    for item in items:
        global file_dict
        ext = item.rfind(".")
        ext_res = item[ext + 1:]
        name_res = item[:ext]
        
        if ext_res in file_dict:
            file_dict.get(ext_res).append(name_res)
        else:
            file_dict[ext_res] = [name_res]

def make_folder():
    global file_dict
    global file_list 
    file_list = list(file_dict.keys())
    parent_folder = "Test"

    for key in file_dict:
        path = os.path.join(parent_folder, key)
        path = os.path.normpath(path)
        if not os.path.isdir(path):
            os.makedirs(path)
    

def move_files():
    global file_list
    global file_dict 
    
    for item in file_list:
        file_name = file_dict.get(item)
        for names in file_name:
            file_path = names + "." + item
            source = os.path.join("Test", file_path)
            destination_folder = os.path.join("Test", item)
            
            os.makedirs(destination_folder, exist_ok=True)
            
            if os.path.isfile(source):
                destination = os.path.join(destination_folder, os.path.basename(source))
                
                shutil.move(source, destination)
        #print(file_name)
    
    