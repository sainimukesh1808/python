# t=()
# t1=(1,)
# t3=1,2,3,4
# print(type(t))
# print(type(t1))
# print(type(t3))
############immutable
# t3[0]=2
# print(t3)
###################
# for i in range(0,len(t3)):
#     print(t3[i])

# t4=(1,[1,2,3],'abs')
# t4[1].append(4)
# t4[1].pop(0)
# print(t4)


######Conversion
# s="Dassault"
# l=[1,2,3]
#
# print(tuple(l))
# print(tuple(s))
# print(s)
#
# t=tuple("absggds")
# print(t)



s=set()
s1={1,2,3}
print(type(s))
print(type(s1))

s2={1,2,3,3,4,5,3,(1,2,3)}
# s3=frozenset({1,2,3,3,4,5,3})
# print(s2)
s3={1,2,3.3,'ab',4}
print(s2|s3)
print(s2 & s3)
print(s2 ^ s3)
# print(s3)
# s2.add(6)
# s2.discard(88)
# print(s2)





