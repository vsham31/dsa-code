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

    void sol(TreeNode* p, vector<int>& ans1){
        if(p==NULL) {
            ans1.push_back(INT_MIN);
            return;
        }

        ans1.push_back(p->val);
        sol(p->left, ans1);
        sol(p->right, ans1);
    }
    
    
    bool isSameTree(TreeNode* p, TreeNode* q) {
    
        vector<int> ans1;
        vector<int> ans2;

        sol(p, ans1);
        sol(q, ans2);

        if(ans1.size()!=ans2.size()) return false;

        for(int i=0; i<ans1.size(); i++){
            if(ans1[i]!=ans2[i]) return false;
        }

        return true;
    
    }
};