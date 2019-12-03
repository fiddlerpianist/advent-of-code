import math

def calculate_fuel(mass):
    return math.floor(mass / 3) - 2

def calculate_fuel_include_fuel_mass(mass):
    fuel = math.floor(mass / 3) - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + calculate_fuel_include_fuel_mass(fuel)

# Part One: What is the sum of the fuel requirements for all of the modules on your spacecraft?
total = 0
with open('day01.txt') as f:
    for line in f:
        total += calculate_fuel(int(line))
print ("Part One: %i" % total)


# Part Two: What is the sum of the fuel requirements for all of the modules on your spacecraft when also taking into account the mass of the added fuel?

total = 0
with open('day01.txt') as f:
    for line in f:
        total += calculate_fuel_include_fuel_mass(int(line))
print ("Part Two: %i" % total)
