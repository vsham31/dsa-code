def fac(i: int, ans: int):
    if i==0:
        return 1

    return ans*fac(i-1, ans+1)

print(fac(5,1))