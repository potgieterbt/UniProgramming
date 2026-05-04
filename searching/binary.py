def binary(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (high + low) // 2
        print(arr[mid])
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = target + 1
        else:
            high = mid - 1


array = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
target = 91
print(binary(array, target))
