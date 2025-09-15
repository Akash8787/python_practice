list1 = [1, 3, 5, 7, 9]
list2 = [2, 4, 6, 8, 10]

len1 = len(list1)
len2 = len(list2)
merge = []
i = 0
j = 0
while i<len1 and j<len2:
    merge+=[list1[i]]
    merge+=[list2[j]]

    i+=1
    j+=1
print(merge)

