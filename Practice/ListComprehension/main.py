# import random
import pandas

# numbers = [1, 2, 3]

# new_numbers = [n * 99999999999999999999 for n in numbers]

# name = "Brian"

# letter_list = [letter for letter in name]

# new_list = [n * 2 for n in range(1, 5)]

# names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]

# short_names = [name for name in names if len(name) < 5]

# long_names_cap = [name.upper() for name in names if len(name) > 4]

# numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

# squared_numbers = [n * n for n in numbers]

#######

# list_of_strings = input().split(',')

# list_of_numbers = [int(s) for s in list_of_strings]

# even_numbers = [n for n in list_of_numbers if n%2 == 0]

# print(even_numbers)

#######

# with open("file1.txt") as file:
#     f1 = [int(line.strip()) for line in file.readlines()]

# with open("file2.txt") as file:
#     f2 = [int(line.strip()) for line in file.readlines()]

# result = [n for n in f1 if n in f2]

# print(result)

#######

# names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]

# students_scores = {student: random.randint(1, 100) for student in names}

# passed_students = {
#     student: score for (student, score) in students_scores.items() if score >= 60
# }

#######

# sentence = input()

# result = {word: len(word) for word in sentence.split()}

# print(result)

#######

# weather_c = {
#     "Monday": 12,
#     "Tuesday": 14,
#     "Wednesday": 15,
#     "Thursday": 14,
#     "Friday": 21,
#     "Saturday": 22,
#     "Sunday": 24,
# }

# weather_f = {day: temp * 9 / 5 + 32 for (day, temp) in weather_c.items()}

#######

# student_dict = {"student": ["Angela", "James", "Lily"], "score": [56, 76, 98]}

# # # Looping through dictionaries:
# # for key, value in student_dict.items():
# #     print(value)

# student_df = pandas.DataFrame(student_dict)
# print(student_df)

# # # Loop through a data frame

# # for (key, value) in student_df.items():
# #     print(value)

# # Loop through rows of a data frame
# for index, row in student_df.iterrows():
#     if row.student == "James":
#         print(row.score)

# passed_student_dict = {
#     row.student: row.score for (index, row) in student_df.iterrows() if row.score > 60
# }
