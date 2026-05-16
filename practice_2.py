"""
Write a program using functions to add two numbers. If the sum of these two numbers is greater than the middle value 
of a user-provided list, print the set of all numbers in the list located between the start and the middle value.
If the sum is equal to the middle value, print a dictionary where the key is the index of the middle value and the 
value is the middle value itself. If the sum is less than the middle value, print a tuple containing all numbers in 
the list that appear after the middle value.[1, 2]
"""


def add(x, y):
    return x + y

a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

lst = list(map(int, input("Enter list elements: ").split()))

s = add(a, b)

mid = len(lst) // 2
mid_value = lst[mid]

if s > mid_value:
    print(set(lst[:mid]))

elif s == mid_value:
    print({mid: mid_value})

else:
    print(tuple(lst[mid + 1:]))
    
    