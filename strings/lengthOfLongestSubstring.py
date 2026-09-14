class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # brute
        ans=0

        for i in range(len(s)):
            hash_set = [0]*256

            for j in range(i, len(s)):
                if hash_set[ord(s[j])]==1:
                    break

                current_len=j-i+1

                hash_set[ord(s[j])]=1

                ans=max(ans, current_len)

        return ans
