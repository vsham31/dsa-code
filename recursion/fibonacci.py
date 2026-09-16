def feb(n: int):
    if n<=1:
        return n
    last = feb(n-1)
    slast= feb(n-2)
    return last + slast

print(feb(4))