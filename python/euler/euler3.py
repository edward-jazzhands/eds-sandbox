# The prime factors of 13195 are 5, 7, 13 and 29.
# What is the largest prime factor of the number 600851475143?

def prime_factorizor(n):

    i = 2                   # we start at two because obviously, its pointless to check if its divisible by 0 or 1
    n_srqroot = n**0.5      # Prime factors cannot be larger than the square root. Law of mathematics. We only need to calculate this one time - because we are getting all prime factors of a *specific* number. So we want the square root of that number to set as our limit.

    prime_factors = []
    while i <= n_srqroot:
        if n % i == 0:                  # if its a factor,
            prime_factors.append(i)     # add to list
            n = n // i                  # divide out the main number
            continue
        else:                           # if its not a factor,
            i += 1                      # iterate +1
    
    if n > 1:                           # if there's a leftover number, it also must be prime
        prime_factors.append(n)

    return prime_factors


n = 600851475143
print(prime_factorizor(n))   # Output for example: [71, 839, 1471, 6857]   Note: this is correct.