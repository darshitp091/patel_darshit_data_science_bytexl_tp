"""
write a program to print the multiple of 5 in three differnt ways in python.
"""

# Method 1: Using for loop

print("Method 1:")
for i in range(1, 11):
    print(i * 5)
    
    
# Method 2: Using while loop

print("Method 2:")
num = 5

while num <= 50:
    print(num)
    num += 5
    

# Method 3: Using lambda function and map

tables = [
    list(map(lambda x: x * 5, range(1, 11))),
    list(map(lambda x: x * 6, range(1, 11))),
    list(map(lambda x: x * 7, range(1, 11)))
]
print(tables)