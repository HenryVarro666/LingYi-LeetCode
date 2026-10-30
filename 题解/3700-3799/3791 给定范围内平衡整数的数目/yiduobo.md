---
title: "3791. 给定范围内平衡整数的数目"
aliases: ["yiduobo的每日leetcode 3791.给定范围内平衡整数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1988667809077675292"
zhihu_id: "1988667809077675292"
zhihu_title: "yiduobo的每日leetcode 3791.给定范围内平衡整数的数目"
question_id: "3791"
question: "给定范围内平衡整数的数目"
problem_url: "https://leetcode.cn/problems/number-of-balanced-integers-in-a-range/"
difficulty: "Hard"
rating: 2132
created: "2025-12-29T22:32:23+08:00"
updated: "2025-12-29T22:32:27+08:00"
upvotes: 1
comments: 0
---

# 3791. 给定范围内平衡整数的数目

> **[yiduobo的每日leetcode 3791.给定范围内平衡整数的数目](https://zhuanlan.zhihu.com/p/1988667809077675292) · 知乎 · 2025-12-29 · 赞同 1**
> 力扣：[3791. 给定范围内平衡整数的数目](https://leetcode.cn/problems/number-of-balanced-integers-in-a-range/) · Hard · 灵茶山艾府：[【模板】上下界数位 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3791.给定范围内平衡整数的数目

[3791. 给定范围内平衡整数的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-balanced-integers-in-a-range/)

题目给出两个正整数low和high，其中low小于等于high，high的大小不超过10^15。

若一个整数至少包含两位数字，且偶数位置上的数字之和恰好等于奇数位置上的数字之和，那么就称其为平衡整数。问low到high之间平衡整数的数量。

非常标准的数位动态规划问题，状态表示也很直观，令f[level][s][state]表示填充了前level位，且填充的偶数位数位之和与奇数位数位之和的差为s，填充数字与上下界的状态为state时的合法填充方案数。

在这里并不需要区分填充的偶数位在原数中是奇数位还是偶数位，因为最终的目标是数位之和相同，因此只需要二者之差为0就行了。在这里也不需要特别判断前导0，因为前导0并不会影响到s。

另外，由于low是正数，因此0会被low排除掉，也就是说不存在合法的1位数整数，无需特别考虑整数至少包含两位数字这个要求。

为了方便计算，在这里需要先将low填充一些前导0，使得low的位数与high相同

对于状态表示中的s，由于s可能小于0，在这里需要加上一个偏移量让其变为非负方便数组下标表示。更进一步的，差值最大的两种情况分别为

909090909090909

以及

190909090909090

差值分别为72以及-62，因此我在这里将s这一维的大小设置为140，然后取65作为偏移量。

而对于其中的state，是一个两位二进制：

- 其中低位表示的是当前填充的前缀是否与low的前缀相同。若相同，那么当前level这一位的填充下界就是low[level]
- 高位表示的则是当前填充的前缀是否与high的前缀相同。若相同，那么当前level这一位的填充上界就是high[level]

对于f[level][s][state]：

1、若level到了high的位数，那么说明填充完成。

若此时的s等于初始的偏移值65，那么f[level][s][state]就是1，否则就是0

2、否则的话需要尝试填充level这一位：

首先需要解析state。若state低位为1，那么当前这一位的下界start就是low[level]，否则就是0；若state高位为1，那么当前这一位的上界end就是high[level]，否则就是9。

接下来从start到end枚举当前这一位填充的值d，对于当前的d：

- 若level为偶数，则将s加上d作为nxt_d，否则将s减去d作为nxt_d
- 若state低位为1，且d与low[level]相同，那么nxt_state的低位也为1，否则为0
- 若state高位为1，且d与high[level]相同，那么nxt_state的高位也为1，否则为0

接下来递归计算f[level + 1][nxt_s][nxt_state]，然后将其累加到f[level][s][state]中即可

计算的入口为f[0][65][3]，其中65为s的偏移量，3为两位二进制的11。

最后附上python代码：

```python
class Solution(object):
    def countBalanced(self, low, high):
        """
        :type low: int
        :type high: int
        :rtype: int
        """
        
        low = [int(x) for x in list(str(low))]
        high = [int(x) for x in list(str(high))]
        n = len(high)
        low = [0] * (n - len(low)) + low

        f = [[[None] * 4 for _ in range(140)] for _ in range(n)]

        def calc(level, s, state):
            if level == n:
                if s == 65:
                    return 1
                return 0
            
            if f[level][s][state] is None:
                f[level][s][state] = 0

                if state & 1:
                    start = int(low[level])
                else:
                    start = 0
                
                if state & 2:
                    end = int(high[level])
                else:
                    end = 9

                for d in range(start, end + 1):
                    if level % 2 == 0:
                        nxt_s = s + d
                    else:
                        nxt_s = s - d
                    
                    nxt_state = 0

                    if (state & 1) and d == low[level]:
                        nxt_state |= 1
                    
                    if (state & 2) and d == high[level]:
                        nxt_state |= 2
                    
                    f[level][s][state] += calc(level + 1, nxt_s, nxt_state)

            return f[level][s][state]
        

        return calc(0, 65, 3)
```
