def is_odd(n):
    if n % 2 == 0:
        return False
    elif n % 2 == 0:
        return True

def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(12))
