# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:

    def sol(self, n: TreeNode | None, arr: List[int]):
        if n==None:
            arr.append(float('-inf'))
            return

        arr.append(n.val)

        self.sol(n.left, arr)
        self.sol(n.right, arr)

    def isSameTree(self, p: TreeNode | None, q: TreeNode | None) -> bool:
        arr1=[]
        arr2=[]
        
        self.sol(p, arr1)
        self.sol(q, arr2)

        if len(arr1)!=len(arr2):
            return False

        # for i in range(len(arr1)):
        #     if arr1[i]!= arr2[i]:
        #         return False

        if arr1!=arr2:
            return False

        return True
