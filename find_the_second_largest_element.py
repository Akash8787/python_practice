l = [40, 30, 20]

# Step 1: Find the largest
first = l[0]
for num in l:
    if num > first:
        first = num
    print("First:",first)

# Step 2: Find the second largest
found = False  # To check if second largest exists
for num in l:
    if num != first:
        second = num
        found = True
        break

if not found:
    print("Second largest does not exist (all elements may be equal).")
else:
    for num in l:
        if num != first and num > second:
            second = num
    print("Second largest element:", second)
