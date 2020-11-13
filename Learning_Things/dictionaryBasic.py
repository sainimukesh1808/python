

user1={"name" : "mukesh", "age" : 24}
user2=dict(name="rakesh", age=24)
user3={
    'name' : 'rohan',
    'age' : 24,
    'fav_movies' : ['SRK',"MSD"],
    'fav_tunes' : ["atif", "abhijit"]
}

# user4={
#     user1 : 'name' : 'rohan',
#     'age' : 24,
#     'fav_movies' : ['SRK',"MSD"],
#     'fav_tunes' : ["atif", "abhijit"]
# }

print(type(user1))


#access data from dict
print(user1['age'])
print(user3)
print(user3['fav_movies'])

#add data in empty dict
user5={}
user5['name']='sachin'
user5['age']=40
print(user5)
