class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        string st = "";
        int n=strs.size();
        sort(strs.begin(), strs.end());

        string first = strs[0];
        string last = strs[n-1];

        int minL=min(first.size(), last.size());

        for(int i=0; i<minL; i++){
            if(first[i]!=last[i]) break;
            st.push_back(first[i]);
        }
        return st;
    }
};