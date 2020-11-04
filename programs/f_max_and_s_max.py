#Find max and second max in a given list without using functions

number_list = [102, 102, 101, 10, 100, -1000]
f_max = max(number_list[0],number_list[1])
s_max = min(number_list[0],number_list[1])

for num in range(2, len(number_list)):
    if(number_list[num]>f_max):
        s_max = f_max
        f_max = number_list[num]
    elif(number_list[num]<f_max and number_list[num]>s_max):
        s_max = number_list[num]
print("first max is {}".format(f_max))
print("second max is {}".format(s_max))
