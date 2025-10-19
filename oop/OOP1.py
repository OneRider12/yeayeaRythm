from typing_extensions import override


class Book:
    def __init__(self, page:int, title:str, color:tuple):
        self._page = page
        self.__title = title
        self.color = color
        print(page, title, color)

    def __open(self): # Abstraction
        pass

    def close(self): # Abstraction
        pass

    def read(self, line): # Abstraction
        # กลาง ไป ขวา
        pass

class NotebookThai(Book): # Inheritance
    def __init__(self, page:int, title:str, color:tuple):
        super().__init__(page, title, color)
        print(self.page, self.__title, self.color)

    @override # Polymorphism
    def read(self, line):
        # ซ้าย ไป ขวา
        pass

    @override # Polymorphism
    def close(self):
        # ปิดหนังสือ
        pass


class NotebookJapan(Book): # Inheritance
    def __init__(self, page:int, title:str, color:tuple):
        super().__init__(page, title, color)
        print(self.page, self.__title, self.color)

    @override
    def read(self, line):
        # ขวา ไป ซ้าย
        pass



class Student:
    def __init__(self, classes):
        self.classes = classes
        self.book = Book(100, "Hello", (255, 255, 255))
        print(self.book.__title, self.book.color)


class Plus:
    def __init__(self, a, b):
        self.c = a + b
        print(self.c)

def calculator():
    a = 1
    b = 2


# book = Notebook(100, "Hello", (255, 255, 255))

student = Student("Cal I")


# line = book.read(4)
# print(line)


# OOP
# Encapsulation
#
# Abstraction
#
# Inheritance
#
# Polymorphism