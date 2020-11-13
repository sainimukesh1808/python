user={
    'name' : 'rohan',
    'age' : 24,
    'fav_movies' : ['SRK',"MSD"],
    'fav_tunes' : ["atif", "abhijit"]
}

#Check if key present or not in dict
if 'age' in user.keys():   #this only check for keys
    print("yes")
else:
    print("no")

#Check if value present or not in dict
if 24 in user.values():
    print("yes")
else:
    print("no")


#Looping

for i in user.keys():
    print(i)                    #will print only key
    print(user[i])              #will print only values


for i in user.values():
    print(i)

for key,value in user.items():
    print(f"key is {key} and value is {value}")



