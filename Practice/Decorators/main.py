# # Functions inputs/functionality/outputs
# def add(n1, n2):
#     return n1 + n2


# def subtract(n1, n2):
#     return n1 - n2


# def multiply(n1, n2):
#     return n1 * n2


# def divide(n1, n2):
#     return n1 / n2


# # Functions are first-class objects, can be passed around as arguments e.g. int/string/float etc.
# def calculate(calc_function, n1, n2):
#     return calc_function(n1, n2)


# result = calculate(multiply, 2, 3)  # 6
# print(result)


# # Nested Functions
# def outer_function():
#     print("I'm the outer function")

#     def nested_function():
#         print("I'm the inner function")

#     nested_function()


# outer_function()


# # Functions can be returned from other functions
# def outer_function2():
#     print("I'm the outer function 2")

#     def nested_function2():
#         print("I'm the inner function 2")

#     return nested_function2


# inner_function = outer_function2()
# inner_function()


# Python Decorators Function
# import time


# # def decorator_function(original_function):
# #     def wrapper_function():
# #         print(f"Wrapper executed this before {original_function.__name__} function")
# #         original_function()

# #     return wrapper_function


# def delay_decorator(function):
#     def wrapper_function():
#         time.sleep(2)
#         # Do something before
#         function()
#         function()
#         # Do something after

#     return wrapper_function


# @delay_decorator
# def say_hello():
#     print("Hello")


# @delay_decorator
# def say_bye():
#     print("Bye")


# def say_greeting():
#     print("How are you?")


# # say_hello()
# # say_greeting()

# decorated_function = delay_decorator(say_greeting)
# decorated_function()

# import time

# current_time = time.time()
# print(current_time)  # seconds since Jan 1st, 1970

# # Write your code below 👇


# def speed_calc_decorator(function):
#     def wrapper_function():
#         start_time = time.time()
#         function()
#         end_time = time.time()
#         print(f"{function.__name__} run speed: {end_time - start_time}s")

#     return wrapper_function


# @speed_calc_decorator
# def fast_function():
#     for i in range(1000000):
#         i * i


# @speed_calc_decorator
# def slow_function():
#     for i in range(10000000):
#         i * i


# fast_function()
# slow_function()


## Advanced Python Decorator Functions
# class User:
#     def __init__(self, name):
#         self.name = name
#         self.is_logged_in = False


# def is_authenticated_decorator(function):
#     def wrapper(*args, **kwargs):
#         if args[0].is_logged_in:
#             function(args[0])
#         else:
#             print("You must be logged in to access this function")

#     return wrapper


# @is_authenticated_decorator
# def create_blog_post(user):
#     print(f"{user.name.capitalize()} has created a new blog post")


# new_user = User("brian")
# new_user.is_logged_in = True
# create_blog_post(new_user)  # You must be logged in to create a blog post

inputs = [1, 2, 3]


def logging_decorator(function):
    def wrapper_function(*args, **kwargs):
        print(f"You called {function.__name__}{args}")
        result = function(*args, **kwargs)
        print(f"It returned: {result}")

    return wrapper_function


@logging_decorator
def a_function(a, b, c):
    return a * b * c


a_function(inputs[0], inputs[1], inputs[2])
