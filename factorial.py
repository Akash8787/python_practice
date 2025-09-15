def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

# Example usage
number = 5
result = factorial(number)
print("Factorial of", number, "is", result)



#without function
number = 5
factorial = 1

if number < 0:
    print("Factorial is not defined for negative numbers.")
elif number == 0:
    print("Factorial of 0 is 1")
else:
    for i in range(1, number + 1):
        factorial *= i
    print("Factorial of", number, "is", factorial)
