---
title: "3751. 范围内总波动值I & 3753. 范围内总波动值II"
aliases: ["yiduobo的每日leetcode 3751.范围内总波动值I && 3753.范围内总波动值II", "3751. 范围内总波动值I", "3753. 范围内总波动值II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/hard", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1976021972736550043"
zhihu_id: "1976021972736550043"
zhihu_title: "yiduobo的每日leetcode 3751.范围内总波动值I && 3753.范围内总波动值II"
question_id: ["3751", "3753"]
question: ["范围内总波动值 I", "范围内总波动值 II"]
problem_url: ["https://leetcode.cn/problems/total-waviness-of-numbers-in-range-i/", "https://leetcode.cn/problems/total-waviness-of-numbers-in-range-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2297
created: "2025-11-23T20:59:34+08:00"
updated: "2025-11-23T20:59:35+08:00"
upvotes: 0
comments: 0
---

# 3751. 范围内总波动值I & 3753. 范围内总波动值II

> **[yiduobo的每日leetcode 3751.范围内总波动值I && 3753.范围内总波动值II](https://zhuanlan.zhihu.com/p/1976021972736550043) · 知乎 · 2025-11-23 · 赞同 0**
> 力扣：[3751. 范围内总波动值 I](https://leetcode.cn/problems/total-waviness-of-numbers-in-range-i/) · Medium · 灵茶山艾府：[两种方法：数位 DP / 数学公式（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3753. 范围内总波动值 II](https://leetcode.cn/problems/total-waviness-of-numbers-in-range-ii/) · Hard · 灵茶山艾府：[两种方法：数位 DP / 数学公式（Python/Java/C++/Go）](../3753%20范围内总波动值%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3751.范围内总波动值I

[3751. 范围内总波动值 I - 力扣（LeetCode）](https://leetcode.cn/problems/total-waviness-of-numbers-in-range-i/description/)

3753.范围内总波动值II

[3753. 范围内总波动值 II - 力扣（LeetCode）](https://leetcode.cn/problems/total-waviness-of-numbers-in-range-ii/description/)

题目给出两个整数num1和num2，其中1 \<\= num1 \<\= num2，表示一个闭区间[num1, nums2]。

一个数字的波动值，定义为这个数字中峰和谷的总数：

- 若某个数位严格大于其两个相邻数位，则称该数位为峰。
- 若某个数位严格小于其两个相邻数位，则称该数位为谷。
- 数字的第一个和最后一个数位不能是峰或者谷。
- 任何少于3位的数字，其波动值均为0。

要求计算[num1, num2]中所有数字的波动值之和。

两题的题设相同，第二题的数据规模较大，num2可达10^15。

由于本题的数据规模较大，因此需要用到数位动态规划。

与常规的数位动态规划不同，若某个数的高位上出现了一个峰或者谷，那么无论低位如何构成，只要其处于num1到num2，这个数的这个峰或者谷都应该被计算。也就是说，在这里需要使用两个数组f和g，其中f记录的是波动值，而g记录的则是处于num1和num2之间元素的个数，那么对于某个state，若此时填充的最后这一位与之前的两位形成了一个峰或者谷，且后续的状态变为了nxt_state，那么除了将f[nxt_state]和g[nxt_state]分别累加到f[state]和g[state]之外，还需要将g[nxt_state]累加到f[state]中，表示这个峰或者谷，在后续所有的g[nxt_state]个数中都需要被计入答案。

为了方便计算，在这里可以先将num1和num2的数位分离出来，得到数位数组d1以及d2，然后在d1的头部填充0，直到d1的长度与d2相同。

接下来分析应该如何设计状态：

首先，因为是一位一位填充的，因此需要记录接下来填充的位level。

接下来，由于需要判断峰和谷，因此需要记录最后填充的两位。不过在这里其实并不需要记录倒数第二位，因为在这里只关心倒数第二位和最后一位的大小关系，因此可以只记录这个大小关系，而不需要记录具体的数值。但是最后填充的这一位必须记录，因为需要知道其具体的数值，才能根据当前填充的这一位来判断大小关系。

最后，由于本题有上下界num1和num2，因此需要一个状态位state，其中最低位和次低位分别表示当前填充的前缀是否顶着下界num1以及是否盯着上界num2。除此之外，还需要记录上面所说的最后两位的大小关系，一共有三种：最后一位小于倒数第二位时为0，相等时为1，最后一位大于倒数第二位时为2。这里三种情况需要两个二进制位。另外，前导0以及最高位没有大小关系这一说，因此可以将这个两位二进制中没用上的那一位利用起来，也就是3用来表示此时还不能讨论大小关系。

综合起来，就是f[level][last_d][state]表示填充了前level位，其中填充的最后一位为last_d，且填充的状态为state时可以得到的波动值，而g[level][last_d][state]则表示可以得到的元素数量。那么对于f[level][last_d][state]以及g[level][last_d][state]：

1、首先可以对state进行分离：

记r \= state // 4，也就是r表示last_d与last_d之前那一位的大小关系。

记upper \= state & 2，表示当前填充的前缀是否顶着num2

记lower \= state & 1，表示当前填充的前缀是否顶着num1

2、接下来确定当前这一位填充的上下界：

若lower为0，说明无需考虑下界num1，此时填充的下界就是0，否则就是d1[level]。

若upper为0，说明无需考虑上界num2，此时填充的上界就是9，否则就是d2[level]。

3、最后尝试填充：

从start开始遍历到end，对于当前遍历到的d，先初始化nxt_state为0，接下来：

若lower为1，且d与d1[level]相同，说明当前的填充方案顶着num1了，需要将1按位或到nxt_state中。

同样的，若upper为1，且d与d2[level]相同，那么就应该将2按位或到nxt_state中。

除此之外，还需要根据当前r来确定是否有波动，以及获取接下来的r：

若当前的r为3且last_d为0，说明目前还处于前导0中，此时的nxt_r也为3。

否则，若当前的d \< last_d，那么nxt_r就为0；若d \= last_d，那么nxt_r就为1；否则nxt_r为2。

若r与nxt_r之和为2，且r不等于1，那么就说明r和nxt_r要么是(2, 0)，要么是(0, 2)，也就是有了波动，此时记delta为1，否则delta为0。

接下来，先递归计算f[level + 1][d][nxt_r \* 4 + nxt_state]以及g[level + 1][d][nxt_r \* 4 + nxt_state]，分别记为df和dg，然后将df + delta \* dg累加到f[level][last_d][state]中，将dg累加到g[level][last_d][state]中即可。

全部计算完成后，f[0][0][15]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def totalWaviness(self, num1, num2):
        """
        :type num1: int
        :type num2: int
        :rtype: int
        """
        
        d2 = [int(x) for x in list(str(num2))]
        n = len(d2)
        d1 = [int(x) for x in list(str(num1))]
        d1 = [0] * (n - len(d1)) + d1

        f = [[[None] * 16 for _ in range(10)] for _ in range(n)]
        g = [[[None] * 16 for _ in range(10)] for _ in range(n)]

        def calc(level, last_d, state, f, g):
            if level == n:
                return 0, 1
            
            if f[level][last_d][state] is None:
                f[level][last_d][state] = 0
                g[level][last_d][state] = 0
                
                r = state // 4
                upper = state & 2
                lower = state & 1

                if lower:
                    start = d1[level]
                else:
                    start = 0
                
                if upper:
                    end = d2[level]
                else:
                    end = 9
                
                for d in range(start, end + 1):
                    nxt_state = 0
                    if lower and d == d1[level]:
                        nxt_state |= 1
                    if upper and d == d2[level]:
                        nxt_state |= 2

                    if r == 3 and last_d == 0:
                        nxt_r = 3
                    elif d < last_d:
                        nxt_r = 0
                    elif d > last_d:
                        nxt_r = 2
                    else:
                        nxt_r = 1
                    
                    if r + nxt_r == 2 and r != 1:
                        delta = 1
                    else:
                        delta = 0

                    df, dg = calc(level + 1, d, nxt_r * 4 + nxt_state, f, g)
                    f[level][last_d][state] += df + delta * dg
                    g[level][last_d][state] += dg
                    
            
            return f[level][last_d][state], g[level][last_d][state]
        
        return calc(0, 0, 15, f, g)[0]
```
