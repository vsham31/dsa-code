class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        maxProfit = 0
        minPrice = float('inf')

        for price in prices:
            if price<minPrice:
                minPrice = price
            else:
                maxProfit = max(maxProfit, price-minPrice)
        # for i in range(len(prices)):
        #     for j in range(i+1, len(prices)):
        #         profit = prices[j]-prices[i]
        #         maxProfit = max(profit, maxProfit)
                    

        return maxProfit


class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        maxProfit = 0

        for i in range(len(prices)):
            for j in range(i+1, len(prices)):
                profit = prices[j] - prices[i]
                maxProfit = max(maxProfit, profit)
                                

        return maxProfit
        