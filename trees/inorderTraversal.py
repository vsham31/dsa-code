# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        arr=[]

        self.fn(root, arr)

        return arr        

    def fn(self, root: Optional[TreeNode], arr):
        if root==None:
            return

        self.fn(root.left, arr)
        arr.append(root.val)
        self.fn(root.right, arr)