import argparse

parser = argparse.ArgumentParser(
    prog='ProgramName',
    description='What the program does',
    epilog='Text at the bottom of help')

parser.add_argument('name', nargs="?", default="World")

args = parser.parse_args()


if __name__ == "__main__":
    print("Hello,", args.name)
    print("Hello, World!")
    print("Hello, Ben!")
