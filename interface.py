#################
### INTERFACE ###
#################
# Abstraction is the seperation between what something does and how it's accomplished.
# Interface: Collection of abstract methods & constants that form the blueprint for classes that implement it.
# Like an abstract class, an interface can't be instantiated and must be implemeted by a class.


from abc import ABCMeta, abstractmethod

# Interface - in this example abstrtact methods ARE used
class AdvancedArithmetic(object, metaclass=ABCMeta):
    # by decorating the abstractmethod, it must be implemented in the class using the interface otherwise exception is raised
    @abstractmethod
    def divisorSum(n):
        raise NotImplementedError

class Calculator(AdvancedArithmetic):
    def divisorSum(self, n):
        x = 0
        for i in range(1,n+1):
            if n % i == 0:
                x += i
        return x

n = int(input())
my_calculator = Calculator()
s = my_calculator.divisorSum(n)
print("I implemented: " + type(my_calculator).__bases__[0].__name__)
print(s)





'''# Interface - in this example abstrtact methods ARE NOT used
class AdvancedArithmetic(object):
    def divisorSum(n):
        raise NotImplementedError

class Calculator(AdvancedArithmetic):
    def divisorSum(self, n):
        x = 0
        for i in range(1,n+1):
            if n % i == 0:
                x += i
        return x


n = int(input())
my_calculator = Calculator()
s = my_calculator.divisorSum(n)
print("I implemented: " + type(my_calculator).__bases__[0].__name__)
print(s)
'''


'''
######################################################
### ABSTRACT METHOD EXAMPLE WITH CLASS INHERITENCE ###
######################################################

from abc import ABCMeta, abstractmethod

class Book(object, metaclass=ABCMeta):
    def __init__(self,title,author):
        self.title=title
        self.author=author   
    @abstractmethod
    def display(): pass

# Write MyBook class
class MyBook(Book):
    
    # Constructor
    def __init__(self, title, author, price):
        super().__init__(title, author)
        self.price = price

    def display(self):
        print(f'Title: {self.title}')
        print(f'Author: {self.author}')
        print(f'Price: {self.price}')

title=input()
author=input()
price=int(input())
new_novel=MyBook(title,author,price)
new_novel.display()
'''