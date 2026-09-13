class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        # brute

        # maxP=float('-inf')

        # for i in range(len(nums)):
        #     pro=1
        #     for j in range(i, len(nums)):
        #         pro=pro*nums[j]
        #         maxP=max(pro, maxP)

        # return maxP


        # optimal
        pre=1
        suf=1
        maxP=float('-inf')
        n=len(nums)

        for i in range(len(nums)):
            if pre==0:
                pre=1
            if suf==0:
                suf=1

            pre=pre*nums[i]
            suf=suf*nums[n-i-1]

            maxP=max(maxP, max(pre, suf))

        return maxP