class Person:
    def __init__(self, firstName, lastName, idNumber):
        self.firstName = firstName
        self.lastName = lastName
        self.idNumber = idNumber
    def printPerson(self):
        print("Name:", self.lastName + ",", self.firstName)
        print("ID:", self.idNumber)

class Student(Person):
    #   Class Constructor
    #   
    #   Parameters:
    #   firstName - A string denoting the Person's first name.
    #   lastName - A string denoting the Person's last name.
    #   id - An integer denoting the Person's ID number.
    #   scores - An array of integers denoting the Person's test scores.
    #
    # Write your constructor here
    def __init__(self, firstName, lastName, idNumber, scores):
        super().__init__(firstName, lastName, idNumber)         # inherits params from Person class

        self.scores = scores

    #   Function Name: calculate
    #   Return: A character denoting the grade.
    #
    # Write your function here
    def calculate(self):
        x = sum(self.scores) / len(self.scores)
        if x >= 90 and x <= 100:
            ans = 'O'
        elif x >= 80 and x < 90:
            ans = 'E'
        elif x >= 70 and x < 80:
            ans = 'A'
        elif x >= 55 and x < 70:
            ans = 'P'
        elif x >= 40 and x < 55:
            ans = 'D'
        elif x < 40:
            ans = 'T'
        return ans


''' input
Heraldo Memelli 8135627
2
100 80
'''

if __name__ == '__main__':
    line = input().split()
    firstName = line[0]
    lastName = line[1]
    idNumber = line[2]

    n = int(input())
    scores = list(map(int, input().rstrip().split()))

    p1 = Person(firstName, lastName, idNumber)
    print(p1.printPerson())
    
    s1 = Student(firstName, lastName, idNumber, scores)
    print(s1.printPerson())
    print(s1.calculate())