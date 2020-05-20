# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:58:36 2020

@author: joeho
"""

"""
Function that changes all the values in a list to a specified value.
"""
def change_list(lst, value):
    
    i = 0
    while i < len(lst):
        
        lst[i] = value 
        i += 1

"""
Function that adds two values.
"""
def add(a, b):
    
    # multiplier
    a = a + 1
    # local scope
    ans = a + b
    
    return ans

if __name__ == "__main__":
    
    a = 2 # Immutable type (unchangeable) # cant challenge that value, and therefore pass by value
    print(a)
    x = add(a, 3) # pass by value i.e. a copy of the original object in memory
    print(a)
    
    l = [4, 5, 6] # Mutable # pass by reference i.e. pass the original memory address of the object
    print(l)
    change_list(l, 5)
    print(l)
    
    l.append(6)
    print(l)
    
    
    print(x)
    
    # Pass by value (Immutable Types e.g. ints, tuples, strings, bool)--> copy of the original value
    # Pass by reference (Mutable Types: lists, dictionaries) --> reference to original object  