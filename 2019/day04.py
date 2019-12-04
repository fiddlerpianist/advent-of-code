# Part One: How many passwords meet the required criteria?
def determineIfCriteriaMetPartOne(num):
    digits = [int(x) for x in str(num)]
    #print (digits)
    if len(digits) != 6:
        return False
    
    foundDoubleDigit = False
    previousDigit = -1
    for i in digits:
        if i < previousDigit:
            return False
        if i == previousDigit:
            foundDoubleDigit = True
        previousDigit = i
    
    #if foundDoubleDigit:
        #print (num)
    return foundDoubleDigit

# Part Two: How many passwords meet the required criteria?
def determineIfCriteriaMetPartTwo(num):
    digits = [int(x) for x in str(num)]
    #print (digits)
    if len(digits) != 6:
        return False
    
    repeatedDigitCount = 1
    foundDoubleDigit = False
    previousDigit = -1
    for i in digits:
        if i < previousDigit:
            return False
        elif i == previousDigit:
            repeatedDigitCount += 1
        elif i > previousDigit:
            # we found an exact sequence of 2. Mark it, then reset
            if repeatedDigitCount == 2:
                foundDoubleDigit = True
            repeatedDigitCount = 1
        previousDigit = i
    
    # In case the double digit is at the end
    if repeatedDigitCount == 2:
        foundDoubleDigit = True

    return foundDoubleDigit

# These were unique to the instance of my puzzle
myGivenLowNUmber = 128392
myGivenHighNumber = 643281

counter = 0
for i in range(128392, 643281 + 1):
    if determineIfCriteriaMetPartOne(i):
        counter += 1
print ("Part One: %i" % counter)

counter = 0
for i in range(128392, 643281 + 1):
    if determineIfCriteriaMetPartTwo(i):
        counter += 1
print ("Part Two: %i" % counter)

