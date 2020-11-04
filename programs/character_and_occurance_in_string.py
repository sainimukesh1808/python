#Write a program to print character and it’s occurrence in a string.
s = "My name is mukesh saini"
char_list = ""
for i in s:
    if(i==" "):
        pass
    else:
        char_list = char_list + i

dict_char_rep = {}
for i in char_list:
    if(i not in dict_char_rep.keys()):
        dict_char_rep[i] = 1
    else:
        dict_char_rep[i] += 1
for key, rep in dict_char_rep.items():
    print("{} {}".format(key, rep))
