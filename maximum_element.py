# # Example list
# my_list = [10, 23, 45, 67, 12, 89, 34]

# # Find maximum element
# max_element = max(my_list)

# print("Maximum element in the list:", max_element)


my_list = [10, 23, 45, 67, 12, 89, 34]

max_element = my_list[0]
second_max_element = my_list[1]

for i in my_list:
    if i>max_element:
        second_max_element=max_element
        max_element = i
    elif i>second_max_element:
        second_max_element = i

print(max_element)
print(second_max_element)
