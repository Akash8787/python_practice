#take user input
String = "Aakash"
for i in String:
    #initialize a count variable
    count = 0
    for j in String:
        #check for repeated characters
        if i == j:
            count+=1
        #if character is found more than 1 time
        #brerak the loop
        if count > 1:
            break
    #print for nonrepeating characters
    if count == 1:
        print(i,end = " ")

# s = "Aakash"

# for ch in s:
#     if s.count(ch) == 1:
#         print(ch, end="")

# rev=""
# for i in s:
#     rev=i+rev
# print(rev)

str1 = String[::-1]
print("str1:",str1)