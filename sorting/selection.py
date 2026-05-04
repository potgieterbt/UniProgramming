def selection(arr):
    n = len(arr)
    for i in range(n):
        minidx = i
        for j in range(i, n):
            if arr[j] < arr[minidx]:
                minidx = j
        if minidx != i:
            arr[minidx], arr[i] = arr[i], arr[minidx]
    return arr
