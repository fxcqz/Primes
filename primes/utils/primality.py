def is_prime(n):
    """Basic primality test for a given number.
    
    See: http://en.wikipedia.org/wiki/Primality_test

    Arguments:
        n -- A number to test the primality of.
    """
    if n <= 3:
        return n >= 2
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n ** 0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True
