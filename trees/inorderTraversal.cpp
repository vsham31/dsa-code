/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> arr;

        fn(root, arr);

        return arr;
    }

    void fn(TreeNode* root, vector<int>& arr){
        if(root==NULL) return;

        fn(root->left, arr);
        arr.push_back(root->val);
        fn(root->right, arr);
    }
};