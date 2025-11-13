import os

file_dict = {}

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
        #grouping(name_res, ext_res)
    print(file_dict)



def grouping(file_name, ext):
    print(file_name, ext)