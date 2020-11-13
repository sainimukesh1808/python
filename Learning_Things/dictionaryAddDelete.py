user={
    'name' : 'rohan',
    'age' : 24,
    'fav_movies' : ['SRK',"MSD"],
    'fav_tunes' : ["atif", "abhijit"],
}

#add data
user['surname']='saini'
print(user)

#pop method
popped_item=user.pop('surname')                 #will return value(datatype will depend on datatype of value) of given key
print(user)
print(f"popped itesm is {popped_item}")


#popitem method
popped_item1=user.popitem()                 #will delete random vale and will return tuple of key, value pair
print(f"popped item 1 is {popped_item1}")
