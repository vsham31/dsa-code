class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        // brute
        int maxLen=0;

        for(int i=0; i<s.size(); i++){
            vector<int> hash(256, 0);

            for(int j=i; j<s.size(); j++){
                if(hash[s[j]]==1) break;
                hash[s[j]]=1;
                maxLen=max(maxLen, j-i+1);
            }
        }
        return maxLen;
    }
};