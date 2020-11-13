# a=[1,2,34,'jhdgbwdacgui', 'kjdcjk123','@#%$',"name", "age"]
# # a[2]=50
# print(a[::-1])
# l=[]
# fruit=['banana', 'apple','mango',123]
# print(type(fruit))
# for i in range(0,len(fruit)):
#     print(fruit[i])
#     print(type(fruit[i]))
# a="anmemamama"
# l1=[]
# for i in a:
#     l1.append(i)
# # l1=a.split("m")
# print(l1)
# a=l1.index('m')
# b=l1.index('m',a+1)
# print(b)

# l=[10,12,13]
# m=[2,3]
# m=l
# print(m)
# print(max(l)-min(l))



# c=l1.pop(2)
# print(c)
# print(l1)
# l2=['a','b','c']
# # l3=l1 + l2
# l1.extend(l2)
# print(l1)
# # print(l2)
# # print(l3)

# l2=[None]*4
# # l2[0]=1
# # l2[1]=1
# # l2[2]=1
# # l2[3]=1
# # l2[4]=1
# print(len(l2))
# for i in l1:
#     l2.append(i*i)
# print(l2)
l=[[1,2],[3,4],['a','b']]
for sublist in l:
    for element in sublist:
        print(element)
