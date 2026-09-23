class Solution:
    def sortedSquares(self, nums: list[int]) -> list[int]:
        # brute
        # for i in range(len(nums)):
        #     nums[i]=nums[i]*nums[i]

        # nums.sort()
        # return nums

        # optimal

        ans=[0]*len(nums)
        left=0
        right=len(nums)-1
        i=right

        for i in range(len(nums)):
            nums[i]*=nums[i]

        while left<=right:
            if nums[left]<nums[right]:
                ans[i]=nums[right]
                i-=1
                right-=1

            else:
                ans[i]=nums[left]
                i-=1
                left+=1

        return ans