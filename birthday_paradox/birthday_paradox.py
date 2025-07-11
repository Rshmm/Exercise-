import datetime, random

def getBirthdays(numbersOfBirthdays):
    """Returns a list of number random date objects for birthdays"""
    birthdays = []
    for i in range(numbersOfBirthdays):
        startOfYear = datetime.date(2001, 1, 1)
        randomNumberOfDays = datetime.timedelta(random.randint(0, 364))
        birthday = startOfYear + randomNumberOfDays
        birthdays.append(birthday)
    return birthdays

def getMatch(birthdays):
    """Returns the date object of a birthday that occurs more than once in the birthdays list """
    if len(birthdays) == len(set(birthdays)):
        return  None #All birthdays are unique, so return None.

    # compare each birthday to every other birthday:
    for a, birthdayA in enumerate(birthdays):
        for b, birthdayB in enumerate(birthdays[a + 1 :]):
            if birthdayA == birthdayB:
                return  birthdayA # Return the matching birthday.


print("""birthday paradox by Al Sweigart

The birthday paradox shows us that in a group of N people, the odds that two of them have matching 
birthdays is surprisingly large. This program dose a Monte Carlo simulation(that is, repeated random 
simulation) to explore this concept.

(It`s not actually a paradox, it`s just a surprising result)

""")


# Set up a tuple of month names in order :
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

while True: #keep asking until the user enters a valid amount.
    print('How many birthdays shall I generate? (Max 100)')
    response = input("> ")
    if response.isdecimal() and (0 < int(response) <= 100):
        numBDays = int(response)
        break # If has entered a valid amount


print()

#  Generate and display the birthdays :
print("Here are", numBDays, "birthdays:")
birthdays = getBirthdays(numBDays)
for i, birthday in enumerate(birthdays):
    if i != 0:
        # Display a comma for each birthday after the first birthday
        print(", ", end='')
        monthName = MONTHS[birthday.month -1]
        dateText = '{} {}'.format(monthName, birthday.day)
        print(dateText, end='')
print()
print()

# Determine if there are two birthdays that match
match = getMatch(birthdays)

# Display that result:
print("In this simulation, ", end='')
if match != None:
    monthName = MONTHS[match.month - 1]
    dateText = '{} {}'.format(monthName, match.day)
    print('multiple people have a  birthday on', dateText)
else:
    print("there are no matching birthdays.")
print()


# Run through 100,000 simulations:
print("Generating", numBDays, "random birthdays 100,000 times .... ")
print("Press Enter to begin ... ")

print("Let\'s run another 100,000 simulatoin.")
simMatch = 0 # How many simulation had matching birthdays in them.
for i in range(100_000):
    # Report on the progress every 10,000 simulations:
    if i % 10_000 == 0:
        print(i, "simulation run ...")
    birthdays = getBirthdays(numBDays)
    if getMatch(birthdays) != None:
        simMatch = simMatch + 1
print("100,000 simulations run.")

# Display simulation result:
probability = round(simMatch / 100_000 * 100, 2)
print("Out of 100,000 simulation of", numBDays, "people, there was a")
print("matching birthday in that group", simMatch, "times. This means")
print("that", numBDays, "people have a", probability, "% chance of")
print("Having matching birthday in their group")
print("that\'s probably more than you would think!" )