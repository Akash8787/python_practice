# An Armstrong number (also called a narcissistic number) is a number that is equal to the sum of its own digits 
# each raised to the power of the number of digits.


for num in range(1, 1001):
    n = len(str(num))
    sum = 0
    temp = num
    while temp > 0:
        digit = temp % 10
        sum += digit ** n
        temp //= 10
    if sum == num:
        print(num)

