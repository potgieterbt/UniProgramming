import argparse

name = "World"


parser = argparse.ArgumentParser(
    prog='ProgramName',
    description='What the program does',
    epilog='Text at the bottom of help')

parser.add_argument('name', required=False)

args = parser.parse_args()


if __name__ == "__main__":
    print("Hello,", args.name)
