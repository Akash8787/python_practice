l=[1,2,3,4,5,10,9,11]

first = l[0]
second = l[1]
for num in l:
    if num>first:
        second=first
        first = num
    elif num > second and num!=first:
        second = num
print("Second_largest:",second)