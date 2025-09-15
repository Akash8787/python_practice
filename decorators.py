# A Python decorator is a function that takes in a function and returns it by adding some functionality.
# Basically, a decorator takes in a function, adds some functionality and returns it.

#==================================================================
def make_pretty(func):                  #func is just a parameter name — you could call it anything else like f, 
                                        # original_function, my_function, etc.
    def inner():                        #It simply refers to the function you’re decorating.                                   
        print("I got decorated")
        func()
    return inner
@make_pretty
def ordinary():
    print("I am ordinary")

# # decorate the ordinary function
# decorated_func = make_pretty(ordinary)

# # call the decorated function
# decorated_func()
ordinary()  

#=================================================================

# def make_pretty1(func):
#     def add(a,b):
#         result = a+b
#         print("Result:",result)
#         func(a,b)
#         return result
        
#     return add
# @make_pretty1
# def addt(a, b):
#     print("success")

# returned_value = addt(3,5)
# print("Returned_Value:",returned_value)
    
     