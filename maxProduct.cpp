    class Solution {
    public:
        int maxProduct(vector<int>& nums) {
            // brute
            // int maxProduct = nums[0];

            // for(int i=0; i<nums.size(); i++){
            //     int product = 1;
            //     for(int j=i; j<nums.size(); j++){
            //         product=product*nums[j];
            //         maxProduct = max(maxProduct, product);
            //     }
            // }   
            // return maxProduct;


            // optimal

            int prefix=1, suffix=1, maxi = INT_MIN, n = nums.size();

            for(int i=0; i<nums.size(); i++){
                if(prefix==0) prefix=1;
                if(suffix==0) suffix=1;

                prefix=prefix*nums[i];
                suffix=suffix*nums[n-i-1];

                maxi = max(maxi, max(prefix, suffix));
            }

            return maxi;
        }
    };