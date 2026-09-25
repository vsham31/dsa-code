class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        minCost=[0]*(len(cost)+1)
        for i in range(2,len(cost)+1):
            minCost[i]=min(cost[i-1]+minCost[i-1], cost[i-2]+minCost[i-2])

        return minCost[len(cost)]