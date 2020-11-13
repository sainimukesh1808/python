###############File objects
import os
os.chdir("D:\\Selenium\\Python")
'''f=open("mk.txt",'r')
print(f.mode)
print(f.name)
f.close()'''
###context manager (automatically close the file after with block)
with open("mk.txt",'r') as f:
    # f_contents1=f.read()   #To read all content of all file
    # f_contents2=f.readlines()   #To read data one by one line, return a list of each line
##To get one line only
    '''f_contents3=f.readline()
    print(f_contents3,end="")   
    f_contents3=f.readline()
    print(f_contents3,end="")'''
##To get whole data line by line
    '''for line in f:            
        print(line,end="")'''
##To get 5 character only
    '''f_contents4=f.read(19)  
    print(f_contents4,end="")
    f_contents4=f.read(5)  #To get next 5 character only
    print(f_contents4)'''

##Just to make above method dynamic
    '''size_to_read = 10     
    f_contents5 = f.read(size_to_read)
    while len(f_contents5)>0:
        print(f_contents5,end="**")
        f_contents5 = f.read(size_to_read)'''
##To get current localtion of cursor (it counts enter as 1 char )
    '''size_to_read = 10
    f_contents5 = f.read(size_to_read)
    print(f_contents5)
    print(f.tell())
    f_contents5 = f.read(size_to_read)
    print(f_contents5)
    print(f.tell())
    f_contents5 = f.read(size_to_read)
    print(f_contents5)
    print(f.tell())
    f_contents5 = f.read(size_to_read)
    print(f_contents5)
    print(f.tell())'''

##To set current localtion of cursor (it also includes enter as 1 char)
    '''f.seek(5)
    size_to_read = 10
    f_contents5 = f.read(size_to_read)
    print(f_contents5)
    print(f.tell())'''
##Writing when file opened in read mode (Will give error)
    f.write("abc")
## to check file is closed or not.
#print(f.closed)

