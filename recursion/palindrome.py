def pal(s: str, i: int, n: int):
    if i>=n/2:
        return True
    if s[i]!=s[n-i-1]:
        return False
    return pal(s, i+1, n)


s='madsm'
print(pal(s,0,len(s)))