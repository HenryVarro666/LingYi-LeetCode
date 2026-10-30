---
title: "2719. 统计整数数目"
aliases: ["yiduobo的每日leetcode 2719.统计整数数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/651972313"
zhihu_id: "651972313"
zhihu_title: "yiduobo的每日leetcode 2719.统计整数数目"
question_id: "2719"
question: "统计整数数目"
problem_url: "https://leetcode.cn/problems/count-of-integers/"
difficulty: "Hard"
created: "2023-08-24T03:33:00+08:00"
updated: "2023-08-24T03:33:00+08:00"
upvotes: 0
comments: 0
---

# 2719. 统计整数数目

> **[yiduobo的每日leetcode 2719.统计整数数目](https://zhuanlan.zhihu.com/p/651972313) · 知乎 · 2023-08-24 · 赞同 0**
> 力扣：[2719. 统计整数数目](https://leetcode.cn/problems/count-of-integers/) · Hard · 灵茶山艾府：[两种数位 DP 模板，附题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2719.统计整数数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-of-integers/)

非常标准的数位动态规划问题，由于数位和的上下界不方便直接放进状态表示中，那么在这里可以采用类似前缀差求解区间问题的方法，令f[level][rest_s][flag]表示从第level个位置开始，后续的数位和不超过rest_s，且前面这些位置与num1和num2的上下界关系为flag。

对于本题flag是一个两位的二进制，其中低位表示当前已经填充的前缀是否与num1的前缀相同，高位表示当前以及填充的前缀是否与num2的前缀相同。对于flag中的低位，若已填充前缀与num1相同，那么对于当前数位上可选数字的下界就是num1中当前位置的值，否则这个下界就是0，反过来对于flag中的高位，若已填充前缀与num2相同，那么对于当前数位上可选数字的上界就是num2中当前位置的值，否则这个上界就是9。

根据上面的状态表示，最终答案就是f[0][max_sum][3] - f[0][min_sum - 1][3]。

接下来是对于f[level][rest_s][flag]的计算。方便起见，我在这里采用的是记忆化搜索的实现方式。

当level来到len(num2)时，说明完成了填充，此时就有f[level][rest_s][flag] \= 1，否则就需要计算f[level][rest_s][flag]：先初始化f[level][rest_s][flag]为0，接下来从0到9遍历当前位上填充的数值digit。若digit大于rest_s，或者digit不在根据flag得到的上下界之内，那么就跳过这个digit，否则就需要先通过digit以及当前的flag计算出填充digit之后的new_flag，然后就有f[level][rest_s][flag] +\= f[level + 1][rest_s - digit][new_flag]。

最后附上python代码：

```python
class Solution(object):
    def count(self, num1, num2, min_sum, max_sum):
        """
        :type num1: str
        :type num2: str
        :type min_sum: int
        :type max_sum: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        n = len(num2)

        global f
        f = [[[None] * 4 for j in range(max_sum + 1)] for i in range(n + 1)]

        def dfs(level, rest_s, flag):
            global f

            if level == len(num2):
                return 1
            
            if f[level][rest_s][flag] is not None:
                return f[level][rest_s][flag]
            
            f[level][rest_s][flag] = 0

            for digit in range(10):
                if digit > rest_s:
                    break
                
                next_flag = 0

                if flag & 1:
                    if digit < int(num1[level]):
                        continue
                    elif digit == int(num1[level]):
                        next_flag |= 1
                
                if flag & 2:
                    if digit > int(num2[level]):
                        continue
                    elif digit == int(num2[level]):
                        next_flag |= 2
                
                f[level][rest_s][flag] += dfs(level + 1, rest_s - digit, next_flag)
                if f[level][rest_s][flag] >= mod:
                    f[level][rest_s][flag] -= mod
            
            return f[level][rest_s][flag]
                

        num1 = '0' * (n - len(num1)) + num1
        res = dfs(0, max_sum, 3) - dfs(0, min_sum - 1, 3)
        if res < 0:
            res += mod
        return res
```
