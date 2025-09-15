#A constructor in Python is a special method used to initialize an object when it is created from a class. 
# In Python, the constructor method is always named __init__.


# class fan:
#     def __init__(self):
#         self.color = "Greeen"
#         self.price = 1500
#         self.brand = "havells"
#         self.no_of_Blades = 3
#     def on(self):
#         print("Fan is on")
#     def off(self):
#         print("Fan is off")
# f1=fan()
# print(f1.color)
#===========================================================

class A:
    def __init__(self, name, age):
        self.name = name
        self.age = age
b=A("aakash",23)
print(b.name)
print(b.age)
#==========================================
# import copy
# class A:
#     def greet(self):
#         return "Hello!"
# b=A()
# a = copy.copy(b) 
# print(b.greet())
# print(id(b)==id(a))
# print(id(a))