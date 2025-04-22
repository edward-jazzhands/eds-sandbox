from typing import Literal, get_args

MyType = Literal["apple", "banana", "cherry"]

my_args: tuple = get_args(MyType)
print(my_args)

# Extract list from the Literal
MY_VALUES: list = list(my_args)

print(MY_VALUES)