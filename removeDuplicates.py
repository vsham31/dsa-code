class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        # brute

        # st=set()

        # for num in nums:
        #     st.add(num)

        # for i, value in enumerate(st):
        #     nums[i]=value

        # return len(st)

        # optimal

        i=0

        for j in range(1,len(nums)):
            if nums[i]!=nums[j]:
                nums[i+1]=nums[j]
                i+=1
        
        return i+1