import math

numbers = [1, 2, 3, 4, 5]
# test comment
for number in numbers:
    print(number)

squared_numbers = [n ** 2 for n in numbers]

print(squared_numbers)

x = 10
if x > 5:
    print("x is greater than 5")
else:
    print("x is 5 or less")

print("float(x):", float(x))

print("math.sqrt(16):", math.sqrt(16))
print("math.pi:", math.pi)

first_name = "John"
second_name = "Doe"

full_name = f"{first_name} {second_name}"
print("Full name:", full_name)

print("The number is " + str(x) + " and its square is " + str(x ** 2))

print(str(x) + first_name)

x = True
y = False

print("x or y =", x or y)    # logical or
print("x and y =", x and y)  # logical and
print("not x =", not x)      # logical not

numbers = [1, 2, 3, 4, 5]
names = ["Janine", "Ali", "Alice"]
mixed = [1, 2, "Max", 3.141]
 
 
names[0]                # get element by index
names[0] = "Peter"      # set element at index
 
print(names[-1])               # use negative indexes to count from the end
 
names.append(-5)        # add element to the end of the list
names.insert(1, "Bob")  # add element at specific index

print(names)

names.remove(-5)        # remove the first occurrence from the list
del names[0]            # remove by index

print(names)

print("Alice" in names)        # check for existence
print("Mario" not in names)    # ... and non-existence

print(numbers.count(1))        # the number of times this item is in the list
print(len(numbers))            # total number of elements in the list

# merge two lists into one
merged = [1, 2, 3] + [4, 5, 6]
print(merged)


pair = ("Tomek", 40)
print(pair[0])  # access first element
print(pair[1])  # access second element
print(pair)      # print the whole tuple

numbers = (1, 2, 3) # tuple of numbers
numbers = list(numbers)  # convert tuple to list
numbers.append(4)  # add an element to the list
print(numbers)  # print the modified list

# dictionaries
grades = {
    "Janine": 5,
    "Ali": 4,
    "Alice": 3,
    "Bob": 2
}
grades = dict(Janine=5, Ali=4, Alice=3, Bob=2)  # another way to create a dictionary

# set

unique_numbers = {1, 1, 2, 3, 4, 5}
print(unique_numbers)  # prints {1, 2, 3, 4, 5}

# iterators only allow getting the next element with next()
r = range(5, 8)
print(r)  # prints range(5, 8)
print(r.start)
print(r.step)
print(r.stop)
r_iterator = r.__iter__()
print(next(r_iterator))  # prints 5
print(next(r_iterator))  # prints 6
print(next(r_iterator))  # prints 7


numbers = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
numbers[5:8]   # give me a new COPY of the list, starting at index 5, and ending at index 7

numbers = [1, -10, 20, 11, 19, 0, -5, -1000, 100, 7]
 
# get a sorted list of the elements
print(sorted(numbers))

print(numbers)
 
# sort the list in-place
numbers.sort()

print(numbers)  # prints the sorted list

names = ["Lisa", "John", "Susan", "Alex"]

for i, name in enumerate(names):
    print(i, name)

prices = [12.3, 5.2, 8.7, 1.2, 8.0]
gross = [price * 1.2 for price in prices if price > 8] # list comprehension with condition

print(gross)  # prints the gross prices for items over 8

def replace(numbers):
    numbers = [11, 12, 13]

numbers = [1, 2, 3]
print(replace(numbers))  # prints None, as the function does not return anything
print(numbers)  # prints the original list [1, 2, 3]