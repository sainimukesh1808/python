'''a=10
def sum():

    a=7
    print(a)

print(a)
sum()
print(a)'''


#############dafault var
'''def full_name(n,m,l=None):
    print(n+" "+m+" "+l)





name=input("enter name ")
mid_name=input("enter middle name")
last_name=input("enter last name")
full_name(name,mid_name,last_name)'''

############
def sum_natural(number):
    sum=0
    for i in range(1,number+1):
        sum=sum+i

    return sum
num=int(input("enter a natural number"))
sum1=sum_natural(num)
print(sum1)

