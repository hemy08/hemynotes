# 买卖股票的最佳时机 II

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-12-02</span>

链接：https://leetcode.cn/leetbook/read/top-interview-questions-easy/x2zsx1/

!!! Question "题目描述"

    给你一个整数数组`prices`，其中`prices[i]`表示某支股票第`i`天的价格。

    在每一天，你可以决定是否购买和/或出售股票。你在任何时候 **最多** 只能持有 **一股** 股票。你也可以先购买，然后在 **同一天** 出售。

    返回你能获得的 **最大** 利润。


!!! example "题目示例"

    === "示例 1："
        **输入：**
        `prices = [7,1,5,3,6,4]`

        **输出：** 7

        **解释：** 
        
        在第 2 天（股票价格 = 1）的时候买入，在第 3 天（股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5 - 1 = 4 。

        随后，在第 4 天（股票价格 = 3）的时候买入，在第 5 天（股票价格 = 6）的时候卖出, 这笔交易所能获得利润 = 6 - 3 = 3 。
            
        总利润为 4 + 3 = 7 。

    === "示例 2："
        **输入：**
        `prices = [1,2,3,4,5]`

        **输出：** 4 

        **解释：** 
        
        在第 1 天（股票价格 = 1）的时候买入，在第 5 天 （股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5 - 1 = 4 。
            
        总利润为 4 。

    === "示例 3："
        **输入：**
        `prices = [7,6,4,3,1]`

        **输出：** 0

        **解释：** 在这种情况下, 交易无法获得正利润，所以不参与交易可以获得最大利润，最大利润为 0 。


!!! tip "提示："
    - $1 <= prices.length <= 3 * 10^4$
    - $0 <= prices[i] <= 10^4$

=== "Go直接解题"

    ```go
    func maxProfit(prices []int) int {
        begin := 0
        end := 0
        profit := 0

        for index := 1; index < len(prices); index++ {
            if prices[index] > prices[end] {
                end = index
                continue
            }

            profit = profit + prices[end] - prices[begin]
            begin = index
            end = index
        }

        profit = profit + prices[end] - prices[begin]
        return profit
    }
    ```

=== "C直接解题"

    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    int maxProfit(const int* prices, int pricesSize) {
        int begin = 0;
        int end = 0;
        int profit = 0;

        for (int index = 1; index < pricesSize; index++) {
            if (prices[index] <= prices[end]) {
                profit = profit + prices[end] - prices[begin];
                begin = index;
            }
            end = index;
        }

        profit = profit + prices[end] - prices[begin];
        return profit;
    }
    ```

=== "Golang优化"

    ```go
    func maxProfit(prices []int) int {
        begin := 0
        end := 0
        profit := 0

        for index, v := range prices {
            if v <= prices[end] {
                profit = profit + prices[end] - prices[begin]
                begin = index
            }

            end = index
        }

        profit = profit + prices[end] - prices[begin]
        return profit
    }
    ```

=== "Golang动态规划一"

    ```go
    func maxInt(a, b int) int {
        if a > b {
            return a
        }

        return b
    }

    func maxProfit(prices []int) int {
        nums := len(prices)
        dp := make([][2]int, nums)

        dp[0][0] = 0
        dp[0][1] = -prices[0]

        for i := 1; i < nums; i++ {
            // 当天手中没有股票 = max（前一天没有股票， 前一天有股票但以今天的价格出售）
            dp[i][0] = maxInt(dp[i-1][0], dp[i-1][1]+prices[i])
            // 当天手中有股票 = max（前一天有股票， 前一天有股票但以今天的价格买入）
            dp[i][1] = maxInt(dp[i-1][1], dp[i-1][0]-prices[i])
        }

        return dp[nums-1][0]
    }
    ```


=== "Golang动态规划二"

    ```go
    func maxInt(a, b int) int {
        if a > b {
            return a
        }

        return b
    }

    func maxProfit(prices []int) int {
        nums := len(prices)

        // 利润，假设前一天手中没有股票
        lastHave := 0 - prices[0]
        lastNoHave := 0

        for i := 1; i < nums; i++ {
            // 当天手中没有股票 = max（前一天没有股票今天不买入， 前一天有股票但以今天的价格出售）
            curNoHave := maxInt(lastNoHave, lastHave+prices[i])
            // 当天手中有股票 = max（前一天有股票今天不出售， 前一天没有股票但以今天的价格买入）
            curHave := maxInt(lastHave, lastNoHave-prices[i])
            lastHave = curHave
            lastNoHave = curNoHave
        }

        return lastNoHave
    }
    ```

=== "C动态规划"

    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    
    #define MAX(a,b) (a) > (b) ? (a) : (b)

    int maxProfitDP(const int* prices, int pricesSize) {
        int dayHave = 0;
        int dayNoHave = 0 - prices[0];

        for (int index = 1; index < pricesSize; index++) {
            // 当天手中有股票 = max（前一天有股票今天不出售， 前一天没有股票但以今天的价格买入）
            int curHave = MAX(dayHave, dayNoHave - prices[index]);
            // 当天手中没有股票 = max（前一天没有股票今天不买入， 前一天有股票但以今天的价格出售）
            int curNoHave = MAX(dayNoHave, dayHave + prices[index]);
            dayHave = curHave;
            dayNoHave = curNoHave;
        }
        return dayNoHave;
    }
    ```