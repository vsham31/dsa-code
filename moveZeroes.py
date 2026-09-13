class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # brute

        # temp = [0] * len(nums)

        # index = 0

        # for i in nums:
        #     if i != 0:
        #         temp[index]=i
        #         index+=1

        # for i in range(len(nums)):
        #     nums[i]=temp[i]

        # optimal

        j=-1

        for i in range(len(nums)):
            if nums[i] == 0:
                j=i
                break

        if j==-1:
            return

        for i in range(j+1, len(nums)):
            if nums[i] !=0:
                nums[i], nums[j] = nums[j], nums[i]
                j+=1

        


        