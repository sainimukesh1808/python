import os
from datetime import datetime
# print(os.getcwd())  ##To get current directory
# os.chdir("D:\Selenium\Python")###to change the directory
# print(os.getcwd())
# print(os.listdir())  # to get list of files/folders present at specific location
# os.mkdir("mukesh.txt")  # to create a folder at current location
# os.makedirs("mukesh_1/mukesh_2") # to create a path and then folder after curren location

# os.rmdir("D:\Selenium\Python\mukesh")    # to delete a folder i.e. will delete only mukesh_2
# os.removedirs("mukesh_1/mukesh_2")   # to delete path and folder as well i.e. will delete both folder
# os.rename("mukesh","ramesh")
########To get information about folder/file
# mod_time=os.stat("mukesh.txt").st_mtime
# print(datetime.fromtimestamp(mod_time))



#########Tree structure
'''for dirpath,dirnames,filenames in os.walk("D:\Selenium\Python\mukesh"):
    #####To print all path,folder,files after path specified above
    print("path : ", dirpath)
    print("folder name : ",dirnames)
    print("filename : ",filenames)
    #####To print all path,folder,files for specific condition
    for i in filenames:
        if i=="mk2.txt":
            print("path",dirpath)
            print("folder name",dirnames)
            print("filename : ", i)
            print()'''
#############All about environment variable
print(type(os.environ.get("TMPDIR")))
print(os.environ.get('TMPDIR'))
print(type(os.environ.get("USER")))
print(os.environ.get('USER'))
# file_path=os.path.join(os.environ.get("TEMP"),"StructuredQuery.log")
# print(file_path)
#
'''print(os.path.exists("/name/mukesh/mk.txt")) ####True if given path
print(os.path.split("/name/mukesh/mk.txt"))#####Returm tuple of path and file name
print(os.path.dirname("/name/mukesh/mk.txt"))
print(os.path.basename("/name/mukesh/mk.txt"))
print(os.path.splitext("/name/mukesh/mk.txt"))'''

#os.rename()
