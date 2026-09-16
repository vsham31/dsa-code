def rev(i: int, arr: list[int], n: int):
    if i>=n/2:
        return

    arr[i], arr[n-i-1] = arr[n-i-1], arr[i]
    rev(i+1, arr, n)

arr=[1,2,3,4,5]
rev(0, arr, len(arr))
print(arr)
