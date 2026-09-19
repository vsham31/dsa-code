from time import perf_counter

def sol(n: int)-> int:
    if n==0 or n==1:
        return 1

    return sol(n-1)+sol(n-2)

def sol1(n: int, dp: list[int])-> int:
    if n==0 or n==1:
        return 1

    if dp[n]!=-1:
        return dp[n]

    dp[n]=sol1(n-1, dp)+sol1(n-2, dp)

    return dp[n]

def sol3(n: int)-> int:
    dp=[-1]*(n+1)
    dp[0]=1
    dp[1]=1

    for i in range(2, n+1):
        dp[i]=dp[i-1]+dp[i-2]

    return dp[n]

def sol4(n: int)-> int:
    prev=1
    prev2=1

    for i in range(2, n+1):
        curri=prev+prev2
        prev2=prev
        prev=curri

    return prev

def print_time(label: str, func):
    start=perf_counter()
    ans=func()
    end=perf_counter()
    print(f'{label}: {ans}, time taken: {end-start:.8f} seconds')

n=33

print_time('ans2 with memoisation recursion', lambda: sol1(n, [-1]*(n+1)))
print_time('ans3 with tabulation', lambda: sol3(n))
print_time('ans4 with array optimsation', lambda: sol4(n))
print_time('ans with raw recursion', lambda: sol(n))
