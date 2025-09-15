l = [2, 3, 4, 5, 1]

maximum = l[0]  # Assume first element is max
for i in l:
    if i > maximum:
        maximum = i

print("Maximum element:", maximum)
