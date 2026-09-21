class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        // // nomal approach
        // set<int> st;

        // for(int i=0; i<nums.size(); i++){
        //     st.insert(nums[i]);
        // }

        // int index=0;
        // for(auto i: st){
        //     nums[index]=i;
        //     index++;
        // }

        // return st.size();

        // optimal

        int i=0;

        for(int j=1; j<nums.size(); j++){
            if(nums[i]!=nums[j]){
                nums[i+1]=nums[j];
                i++;
            }
        }
        return i+1;
    }
};