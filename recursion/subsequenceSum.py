def fn(i: int, arr: list[int], nums: list[int], sum: int, target: int):
    if i==len(nums):
        if sum==target:
            print(arr)
        return

    arr.append(nums[i])
    sum+=nums[i]
    fn(i+1, arr, nums, sum, target)

    arr.remove(nums[i])
    sum-=nums[i]
    fn(i+1, arr, nums, sum, target)

print('Answer for all the subsequences: ')
fn(0, [], [1,2,1], 0, 2)

def oneSubsequence(i: int, arr: list[int], nums: list[int], sum: int, target: int)-> bool:
    if i==len(nums):
        if sum==target:
            print(arr)
            return True
        return False

    arr.append(nums[i])
    sum+=nums[i]
    if oneSubsequence(i+1, arr, nums, sum, target) == True:
        return True

    arr.remove(nums[i])
    sum-=nums[i]
    if oneSubsequence(i+1, arr, nums, sum, target) == True:
        return True

    return False

print('\nAnswer for only 1 subsequence: ')
oneSubsequence(0, [], [1,2,1], 0, 2)