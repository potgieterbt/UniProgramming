total_marks = 75
students = ["Bob Dylan", "Porter Testa", "Zack Dorion", "Jamey Connette"]
grades = [
    [50, 40],
    [21],
    [36],
    [66, 20],
]
percentages = []
for student_index in range(len(students)):
    percentages.append([])
    for grade_index in range(len(grades[student_index])):
        percentages[student_index].append(
            round((grades[student_index][grade_index] / total_marks)*100, 2))

if __name__ == "__main__":
    should_close = False
    menu_index = 0
    while should_close is False:
        if menu_index == 0:
            try:
                option = int(input("""1 - Edit Data
2 - List Grades
3 - Exit
"""))
            except ValueError:
                print("invalid input, please input a number")
                continue
            match(option):
                case 1:
                    menu_index = 2
                    continue
                case 2:
                    menu_index = 1
                    continue
                case 3:
                    print("Good Bye")
                    should_close = True

        elif menu_index == 1:
            try:
                option = int(input(
                    """1 - List all marks as percentages
2 - List highest mark
3 - List lowest mark
4 - List the range of marks
5 - List the average mark
6 - List grade achievmement amounts
7 - List number of fails
8 - Back
9 - Exit
~ """))
            except ValueError:
                print("invalid input, please input a number")
                continue

            match(option):
                case 1:
                    for student_index in range(len(students)):
                        print(students[student_index], "- ", end="")
                        for grade_index in range(len(grades[student_index])):
                            print(percentages[student_index]
                                  [grade_index], end="")
                            if grade_index + 1 < len(grades[0]):
                                print(", ", end="")
                        print("")
                case 2:
                    highest_student_index = []
                    highest_grade = -1
                    highest_percentage = -1
                    for student_index in range(len(students)):
                        for grade_index in range(len(grades[student_index])):
                            if grades[student_index][grade_index] > highest_grade:
                                highest_grade = grades[student_index][grade_index]
                                highest_percentage = percentages[student_index][grade_index]
                                highest_index = grade_index
                                highest_student_index.clear()
                                highest_student_index.append(student_index)
                            elif grades[student_index][grade_index] == highest_grade:
                                highest_student_index.append(student_index)
                    print(
                        "Grade: ", highest_grade, ",", str(highest_percentage) + "%")
                    print("Student(s): ", end="")
                    for student_index in highest_student_index:
                        print(students[student_index])

                case 3:
                    lowest_student_index = []
                    lowest_grade = total_marks + 1
                    lowest_percentage = 101

                    for student_index in range(len(students)):
                        for grade_index in range(len(grades[student_index])):
                            if grades[student_index][grade_index] < lowest_grade:
                                lowest_grade = grades[student_index][grade_index]
                                lowest_percentage = percentages[student_index][grade_index]
                                lowest_index = grade_index
                                lowest_student_index.clear()
                                lowest_student_index.append(student_index)
                            elif grades[student_index][grade_index] == lowest_grade:
                                lowest_student_index.append(student_index)
                    print(
                        "Grade: ", lowest_grade, ",", str(lowest_percentage)+"%")
                    print("Student(s): ", end="")
                    for student_index in lowest_student_index:
                        print(students[student_index])

                case 4:
                    highest_grade = -1
                    highest_percentage = -1
                    lowest_grade = total_marks + 1
                    lowest_percentage = 101
                    for student_index in range(len(students)):
                        for grade_index in range(len(grades[student_index])):
                            if grades[student_index][grade_index] < lowest_grade:
                                lowest_grade = grades[student_index][grade_index]
                                lowest_percentage = percentages[student_index][grade_index]
                            if grades[student_index][grade_index] > highest_grade:
                                highest_grade = grades[student_index][grade_index]
                                highest_percentage = percentages[student_index][grade_index]
                    print("Range(Raw Marks):", lowest_grade, "-", highest_grade,
                          ":", highest_grade - lowest_grade)
                    print("Range(Percentages):", str(lowest_percentage) + "%", "-", str(highest_percentage) + "%",
                          ":", str(highest_percentage - lowest_percentage)+"%")
                case 5:
                    count = 0
                    sum = 0
                    percentage_sum = 0
                    for student_index in range(len(students)):
                        for grade_index in range(len(grades[student_index])):
                            count += 1
                            sum += grades[student_index][grade_index]
                            percentage_sum += percentages[student_index][grade_index]
                    print("Average(Raw Marks):", round(sum / count, 2))
                    print("Average(Percentages):", str(round(
                        percentage_sum / count, 2))+"%")
                case 6:
                    As = 0
                    Bs = 0
                    Cs = 0
                    Ds = 0
                    Es = 0

                    for student_index in range(len(students)):
                        for grade_index in range(len(grades[student_index])):
                            percentage = int(
                                percentages[student_index][grade_index])
                            if percentage in range(40, 50):
                                Es += 1
                            if percentage in range(50, 60):
                                Ds += 1
                            if percentage in range(60, 70):
                                Cs += 1
                            if percentage in range(70, 80):
                                Bs += 1
                            if percentage in range(80, 101):
                                As += 1
                    print("A's:", As)
                    print("B's:", Bs)
                    print("C's:", Cs)
                    print("D's:", Ds)
                    print("E's:", Es)
                case 7:
                    fail_count = 0
                    for student_index in range(len(students)):
                        for grade_index in range(len(grades[student_index])):
                            percentage = int(
                                percentages[student_index][grade_index])
                            if percentage < 40:
                                fail_count += 1
                    print("Fails:", fail_count)

                case 8:
                    menu_index = 0
                case 9:
                    print("Good Bye")
                    should_close = True
                case _:
                    print("Please input a valid number")
        elif menu_index == 2:

            try:
                option = int(input("""1 - Add Student
2 - Remove Student
3 - Edit Student
4 - Back
5 - Exit
"""))
            except ValueError:
                print("invalid input, please input a number")
                continue
            match(option):
                case 1:
                    menu_index = 3
                case 2:
                    menu_index = 4
                case 3:
                    menu_index = 5
                case 4:
                    menu_index = 0
                case 5:
                    print("Good Bye")
                    should_close = True
        elif menu_index == 3:
            # Add Student
            input("Please enter Student's full name: ")
            while (grade := input("Please enter the grade(enter q to finish):")):
                try:
                    grade = int(grade)
            except ValueError:
                print("invalid input, please input a number")
                continue
        elif menu_index == 4:
            # Remove Student
        elif menu_index == 5:
            # Edit Student
