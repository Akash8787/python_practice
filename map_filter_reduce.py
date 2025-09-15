l=[2,3,4,5,6,7]
# def cube(x):
#     return x*x*x
# newl=[]
# for i in l:
#     newl.append(cube(i))
# print(newl)

# map(function, iterable)
# Applies the given function to each item in the iterable.
# Returns a map object (which you can turn into a list).

# #after using MAP function
# newl=list(map(lambda x:x*x*x,l))
# print(newl)

# #FILTER
# def filter_fun(a):
#     return a>4
# newl=list(filter(filter_fun,l))
# print(newl)


# The reduce function applies the function to the first two elements in the iterable 
# and then applies the function to the result and the next element, 
# and so on. The reduce function returns the final result.

from functools import reduce
l=[2,3,4,5,6,7]
newl=reduce(lambda x,y:x+y,l)
print(newl)


# filter(function, iterable)
# Filters elements in the iterable using the function that returns True or False.
# Returns a filter object (convert to list to see results).


# nums = [1, 2, 3, 4, 5]
# l =[]
# for i in nums:
#     if i%2==0:
#         l.append(i)
# print(l)



# evens = list(filter(lambda x: x % 2 == 0, nums))
# print(evens)  # Output: [2, 4]
