class Solution:

    def sol(self, s: str, t: str, ans: str, i: int)-> bool:
        if i>=len(t):
            return ans==s

        if ans==s:
            return True

        ans+=t[i]

        if self.sol(s,t,ans,i+1) == True:
            return True

        ans=ans[:-1]
        if self.sol(s,t,ans,i+1) == True:
            return True

        return False


    def isSubsequence(self, s: str, t: str) -> bool:
    # brute
        
        return self.sol(s, t, "", 0)

    # optimal
        # i=0
        # j=0

        # while i<len(s) and j<len(t):
        #     if s[i]==t[j]:
        #         i+=1
        #         j+=1
        #     else:
        #         j+=1

        # if i==len(s):
        #     return True
        # else:
        #     return False
    
        