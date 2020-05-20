
# Data structure: Dictionary
# {key: value, key: value}

our_dict = {"hey": 1, "hello": 2}

value = our_dict["hello"]

#print("Value: {}".format(value))

# Recursion:
# 5! = 5 x 4 x 3 x 2 x 1

def factorial(num):

    print(num)

    # base case
    if num == 1:
        return num

    # recursive step
    return num * factorial(num - 1)

ans = factorial(5)
print(ans)

