names = ["Sewing Thread (100m)", "Zipper(20cm)", "Wooden Buttons(Pack of 10)", "Iron-on Interfacing(1m)", "Bias Binding(2.5m)",
         "Hook and Eye Set(10 pairs)", "Seam Ripper", "Tailor's Chalk(3-pack)", "Elastic(1m, 25mm width)", "Thimble(Metal)"]
prices = [1.2, 0.65, 1.8, 2.5, 1.1, 0.9, 1.5, 1.25, 0.75, 1]
stock = [184, 97, 142, 76, 213, 58, 34, 89, 167, 121]

total_value = 0

if __name__ == "__main__":
    should_close = False
    while should_close is False:
        try:
            option = int(input(
                "1 - List Items\n2 - Add Item\n3 - Edit Item\n4 - Delete Item\n5 - Exit\n"))
        except ValueError:
            print("invalid input, please input a number")
            continue

        match(option):
            case 1:
                for i in range(len(names)):
                    print(names[i])
                    print(prices[i])
                    print(stock[i])
                    total_value += prices[i] * stock[i]

                print("The total value of the stock is:", total_value)
            case 2:
                name = input()
                price = float(input())
                quantity = int(input())

                names.append(name)
                prices.append(price)
                stock.append(quantity)

            case 3:
                for i in range(len(names)):
                    print(i, "-", names[i])
                idx = int(input("Input the number of the product to edit"))

            case 4:
                for i in range(len(names)):
                    print(i, "-", names[i])
                idx = int(input("Input the number of the product to delete"))
            case 5:
                should_close = True
