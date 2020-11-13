import os
os.chdir("D:\\Selenium\\Python")


'''with open("mk1.txt","w") as f:   #if file is not present it will create automatically on specified path
    f.write("text")
    f.seek(0)
    f.write("R")'''

## read a file and copy another file
'''with open("mk.txt","r") as rf:
    print(rf.read())
    with open("mk_copy.txt",'w') as wf:
        for line in rf:
            wf.write(line)'''

##To create copy of images
'''with open("mk.png","rb") as rf:
    print(rf.read())
    with open("mk_copy.png",'wb') as wf:
        for line in rf:
            wf.write(line)'''

