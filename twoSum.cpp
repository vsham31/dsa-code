// better

unordered_map<int, int> mp;

        for(int i=0; i<len; i++){
            int complement = target-nums[i];

            if(mp.find(complement) != mp.end()) return {mp[complement], i};

            mp[nums[i]]=i;
        }

        return {-1,-1};

// optimised


        vector<pair<int, int>> arr;

        for(int i=0; i<len; i++) arr.push_back({nums[i], i});

        sort(arr.begin(), arr.end());

        int left = 0, right = len-1;

        for(int i=0; i<len; i++){
            int sum = arr[left].first + arr[right].first;
            if(target == sum) return {arr[left].second, arr[right].second};
            else if(sum < target) left++;
            else right--;
        }

        return {-1,-1};