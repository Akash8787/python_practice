# n=5
# for i in range(n):
#     for j in range(n):
#         print("*",end=" ")
#     print()


# for i in range(n):
#     for j in range(i+1):
#         print("*",end=" ")
#     print()

# for i in range(n):
#     for j in range(i,n):
#         print(" ",end=" ")
#     for j in range(i+1):
#         print("*",end=" ")
#     print()

# for i in range(n):
#     for j in range(n-i):
#         print("*", end=" ")
#     for j in range(i+1):
#         print("@",end=" ")
#     print()


# n = int(input("Enter the number of lines to be printed: "))

# # Upper part of the pattern
# for i in range(1, n + 1):
#     for j in range(n - i):
#         print(" ", end="")
#     for j in range(2 * i - 1):
#         if j == 0 or j == 2 * i - 2:
#             print("*", end="")
#         else:
#             print(" ", end="")
#     print()

# # Lower part of the pattern
# for i in range(n - 1, 0, -1):
#     for j in range(n - i):
#         print(" ", end="")
#     for j in range(2 * i - 1):
#         if j == 0 or j == 2 * i - 2:
#             print("*", end="")
#         else:
#             print(" ", end="")
#     print()



s = input("Enter the String: ")

print(s)  # Print the original string

length = len(s)

# From index 1 to length - 2 (excluding first and last character)
for i in range(1, length - 1):
    left_char = s[i]
    right_char = s[length - 1 - i]
    print(left_char + ' ' * (length - 2) + right_char)

# Print reversed string at the end
print(s[::-1])


