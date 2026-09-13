    class Solution {
    public:
        void moveZeroes(vector<int>& nums) {
            // brute
            // vector<int> temp(nums.size(), 0);
            // int index = 0;

            // for(int i=0; i<nums.size(); i++){
            //     if(nums[i]!=0) {
            //         temp[index] = nums[i];
            //         index++;
            //     }
            // }

            // for(int i=0; i<nums.size(); i++){
            //     nums[i]=temp[i];
            // }
            
    // optimal

            int j=-1;

            for(int i=0; i<nums.size(); i++){
                if(nums[i]==0){
                    j=i;
                    break;
                }
            }

            if(j==-1) return;

            for(int i=j+1; i<nums.size(); i++){
                if(nums[i]!=0) {
                    swap(nums[i], nums[j]);
                    j++;
                }
            }
        }

    };