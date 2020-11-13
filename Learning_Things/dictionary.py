d1={1:"mukesh",2:"saini","Company":"DS",3:12,4:"mk"}
'''print(type(d1))'''
print(d1)
######Accessing element/keys/values

'''print(d1.keys())
print(d1.values())
print(d1[1])
print(d1["Company"])
print(d1.get("Company"))
print(d1.items())'''    #Returns a list of dict’s (key, value) tuple pairs
#########Adding element
'''d1[5]=14
d1[6]="mk"
print(d1)
d1[7]=(1,2,3,4)
print(d1)'''
########updating element
'''d1[4]="mk1"
print(d1)'''
#######removing elements
'''del d1[3]
print(d1)

d1.pop(1)
print(d1)

d1.popitem()    #Last key:pair will deleted
print(d1)


d1.clear()'''        #To delete entire dict
##########looping
for key in d1.keys():
    print(key)
for value in d1.values():
    print(value)
for key,value in d1.items():
    print(key,":",value)
    #print(value)
