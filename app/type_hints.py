value = "value"

value: int = 12.3

print(pow(value, 2))

text: str = "value"
perc: int = 80
temp: float = 37.5

numbers: list[int] = [1, 2, 3, 4, 5]

tuple_5: tuple[int] = (1, 2, 3, 4, 6, "key")


# throws error
# tuple_5.add(7)

print(tuple_5)


class City:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    # This method tells Python how to represent the object as a string
    def __repr__(self):
        return f"City : {self.name} at location {self.location}"


city = City("Mumbai", 123445)
tupple_city: tuple[City, int] = (city, 123)
print(tupple_city)
