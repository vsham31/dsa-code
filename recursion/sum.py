def add(i: int, sum: int):
    if i==0:
        return 0

    return sum+add(i-1, sum+1)

print(add(3, 1))