def fn(index: int, arr: list[int], nums: list[int]):
    if index>=len(nums):
        print(arr)
        return

    arr.append(nums[index])
    fn(index+1, arr, nums) # take
    arr.remove(nums[index])
    fn(index+1, arr, nums) # not take

fn(0, [], [3,1,2])