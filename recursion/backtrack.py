def fn(i: int, n: int):
    if i<n:
        return

    fn(i-1, n)
    print(i)


fn(6, 0)