# l = [2, 3, 4, 5, 5]
# unique = []

# for i in l:
#     if i not in unique:
#         unique.append(i)

# print(unique)


s='Aakash'
result = ""
for i in range(len(s)):
    char = s[i]
    found = False

    # Check if char is already in result
    for j in range(len(result)):
        if result[j] == char:
            found = True
            break

    if not found:
        result += char

print(result)

