# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        arr=[]

        self.fn(root, arr)

        return arr
        

    def fn(self, root: Optional[TreeNode], arr:List[int]):

        if root==None:
            return
        arr.append(root.val)
        self.fn(root.left, arr)
        self.fn(root.right, arr)