def fibonacci(n):
    fib_sequence = [0, 1]  # Initialize the sequence with the first two terms
    for i in range(2, n):
        next_term = fib_sequence[-1] + fib_sequence[-2]
        fib_sequence.append(next_term)
    return fib_sequence

# Example usage
num_terms = 10
fib_sequence = fibonacci(num_terms)
print("Fibonacci sequence up to", num_terms, "terms:", fib_sequence)
