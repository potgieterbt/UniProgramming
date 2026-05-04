import csv
import os

cars = []


def list_all_cars():
    if len(cars) == 0:
        print("The list is empty")
        return
    for index in range(len(cars)):
        print("Index", str(index) + ":", cars[index])


def add_car_to_list(reg):
    reg = reg.upper()
    cars.append(reg)
    print("Registration", reg, "added to list")


def get_index_from_user():
    size = len(cars)
    index = -1
    while 1:
        index = input("Please input a number between 0 and " +
                      str(size - 1) + "(enter q to quit): ")
        if index == 'q':
            return -1
        try:
            index = int(index)
        except ValueError:
            print("invalid input, please input a number")
            continue
        if index >= 0 and index < size:
            break

    return index


def validate_reg(reg):
    if len(reg) == 9 and reg[0] == '\ufeff':
        reg = reg[1:]
    if len(reg) != 8:
        return False
    parts = reg.split(" ")
    if len(parts[0]) != 4 or len(parts[1]) != 3:
        return False
    elif not (parts[0][0:2].isalpha() and parts[0][2:4].isnumeric()):
        return False
    elif not (parts[1][0:4].isalpha()):
        return False
    else:
        return True


def get_reg_from_user():
    while 1:
        reg = input(
            "Please input the registration of the car(in format: AA11 AAA) enter q to quit: ")
        if reg == 'q':
            return reg
        if not validate_reg(reg):
            print("Registration not valid please try again")
            continue
        else:
            return reg


def print_car_at_index():
    if len(cars) == 0:
        print("The list is empty")
        return

    index = get_index_from_user()
    if index == -1:
        print("No input given")
        return
    print("Index", str(index) + ":", cars[index])


def get_file_path_from_user():
    base_path = os.path.abspath(os.getcwd())
    path = input(
        "Please input the relative path to the file(input -1 it quit): ")
    if path == "-1" or path == '':
        return -1
    path = os.path.join(base_path, path)

    return path


def add_from_csv():
    path = get_file_path_from_user()
    if path == -1:
        print("File path not input")
        return

    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not validate_reg(row[0]):
                continue
            else:
                cars.append(row[0])
                print(row[0])
    print("Successfully added cars from csv")


def download_to_txt():
    path = get_file_path_from_user()
    if path == -1:
        print("File path not input")
        return

    open(path, 'w').close()
    with open(path, 'a') as file:
        for index in range(len(cars)):
            string = "Index " + str(index) + ":" + cars[index]
            file.write(string)
            file.write("\r\n")


if __name__ == "__main__":
    should_close = False
    menu_index = 0
    while should_close is False:
        if menu_index == 0:
            try:
                option = int(input("""1 - Add Car
2 - List All Cars
3 - List Car At Index
4 - Add From CSV
5 - Download To File
6 - Exit
~ """))
            except ValueError:
                print("invalid input, please input a number")
                continue
            except KeyboardInterrupt:
                option = 6
            match(option):
                case 1:
                    reg = get_reg_from_user()
                    if reg == 'q':
                        print("No input provided")
                        continue
                    add_car_to_list(reg)
                    continue
                case 2:
                    list_all_cars()
                    continue
                case 3:
                    print_car_at_index()
                case 4:
                    add_from_csv()
                case 5:
                    download_to_txt()
                case 6:
                    print("Good Bye")
                    should_close = True
