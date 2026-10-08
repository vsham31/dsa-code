# Question 1 — Find non-repeating characters

l1=["abcdefghibcaewb"]

ans=""

for i in range(len(l1[0])):
    if l1[0].count(l1[0][i])==1:
        ans+=(l1[0][i])

print(ans)

