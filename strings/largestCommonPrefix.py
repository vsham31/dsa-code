class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        strs.sort()
        st=""

        first=strs[0]
        last=strs[-1]

        for i in range(min(len(first), len(last))):
            if first[i]!=last[i]:
                break

            st+=first[i]

        return st