class Solution {
public:

    bool sol(string s, string t, string ans, int i){
        
        // brute

        if(i>t.size()) return false;

        if(ans==s) return true;


        ans+=t[i];
        if(sol(s, t, ans, i+1) == true) return true;

        ans.pop_back();
        if(sol(s, t, ans, i+1) == true) return true;

        return false;
    }

    bool isSubsequence(string s, string t) {
        string ans;
        // return sol(s,t,ans,0, p);
        // optimal
        int i=0,j=0;

        while(i<t.size() && j<s.size()){
            if(s[j]==t[i]){
                j++;
                i++;
            } else {
                i++;
            }
        }

        if(j==s.size()) return true;
        return false;
    }
};