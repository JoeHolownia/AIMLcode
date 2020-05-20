# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:19:50 2020

@author: joeho
"""
# Global scope

# Variables
a = 1
b = 2 # int
hello = "Hello" # string
true = True #bool
true = "Hello"
false = False
c = 4.78990

# My preferred method
# print("Our value for a is {}, and our value for b is {}".format(a, b))

# String concatenation
# print("Hello" + str(a))
# print("Hey ", a, b)

# Control: if/else (conditionals)

"""if b > a:
    # local scope
    print("b is greater than a")
    print(a)
    
else:
    print("a is greater than b")
"""

# Loops: for/while

# While Loop
i = 0 # iterator/counter
while i < 10:
    #print(i)
    # code in here
    i += 1 # increment i
    
# For each loop
numbers = [1, 3, 5, 7, 8]

for number in numbers:
    
    number = 2
    print(number)
    
print(numbers)

# While loop for list access
j = 0
while j < len(numbers):
    
    numbers[j] = 1
    item = numbers[j]
    print("Item in numbers: {}".format(item))
    j += 1

print(numbers)
print(len(numbers))

# Data Structures:
"""
    variable = 1
    list = [0, 1, 2]
    tuple = (0, 1, 2) # Can't change this
    
"""

a_list = ["string", 1, 2, False] # can change this: Mutable type
a_tuple = (0, 1, 2) # Can't change this: Immutable type

# In python, '0 indexing'
# print(a_list[0])

a_list[0] = 3

# print("Tuple: {}".format(a_tuple))


# a_tuple[0] = 5 # CANNOT DO THIS!

# print(a_list)
# print(a_tuple)


    