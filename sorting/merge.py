def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[0..mid])
    right = merge_sort(arr[mid + 1:])
    return merge(left, right)
    pass


def merge(left, right):
    pass
