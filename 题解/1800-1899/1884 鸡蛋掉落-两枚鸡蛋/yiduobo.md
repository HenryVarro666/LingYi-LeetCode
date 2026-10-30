---
title: "1884. 鸡蛋掉落-两枚鸡蛋"
aliases: ["yiduobo的每日leetcode 1884.鸡蛋掉落-两枚鸡蛋"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/477328025"
zhihu_id: "477328025"
zhihu_title: "yiduobo的每日leetcode 1884.鸡蛋掉落-两枚鸡蛋"
question_id: "1884"
question: "鸡蛋掉落-两枚鸡蛋"
problem_url: "https://leetcode.cn/problems/egg-drop-with-2-eggs-and-n-floors/"
difficulty: "Medium"
created: "2022-03-07T23:25:57+08:00"
updated: "2022-03-07T23:25:57+08:00"
upvotes: 3
comments: 0
---

# 1884. 鸡蛋掉落-两枚鸡蛋

> **[yiduobo的每日leetcode 1884.鸡蛋掉落-两枚鸡蛋](https://zhuanlan.zhihu.com/p/477328025) · 知乎 · 2022-03-07 · 赞同 3**
> 力扣：[1884. 鸡蛋掉落-两枚鸡蛋](https://leetcode.cn/problems/egg-drop-with-2-eggs-and-n-floors/) · Medium · 灵茶山艾府：[两种方法：动态规划/数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1884.鸡蛋掉落-两枚鸡蛋

[力扣](https://leetcode-cn.com/problems/egg-drop-with-2-eggs-and-n-floors/)

经典的动态规划问题，之前一枚鸡蛋的版本我偷懒写了个最朴素的动态规划，这次换个高级点的。

同样是先转换思路，不考虑确定f的最小操作次数，而是令g[i][j]表示i枚鸡蛋，丢j次可以确定的最大高度，然后通过g[i][j]与n的大小确定j的最小值，即为最终答案。

对于g[i][j]：

1、同样是先考虑边界情况。当i \= 1时，只有一枚鸡蛋，因此扔j次最多确定j层楼。当j \= 1时，由于只能扔一次，那么无论是多少次扔的机会，也只能确定1层楼，即

g[1][j] \= j

g[i][1] \= 1

2、对于一般情况

不妨设k \= g[i - 1][j - 1]，那么第j次操作可以选择在第k + 1层扔。如果蛋碎了，那么就回归到了g[i - 1][j - 1]的情况。若没有碎，那么还可以往上再确认g[i][j - 1]层，于是就有

g[i][j] \= g[i - 1][j - 1] + 1 + g[i][j - 1]

对于本题，两枚鸡蛋，就有

g[2][j] \= g[1][j - 1] + 1 + g[2][j - 1]

根据上面的g[1][j] \= j，就有g[1][j - 1] \= j - 1

g[2][j] \= j - 1 + 1 + g[2][j - 1] \= g[2][j - 1] + j

而g[2][1] \= 1，所以实际上

g[2][j] \= 1 + 2 + ... + j \= (1 + j) \* j / 2

也就是说两枚鸡蛋扔j次，最多可以确认高度为(1 + j) \* j / 2这个高度的楼，那么此时只需要找出最小的j，满足

(1 + j) \* j / 2 >\= n

解出来就是

j >\= sqrt(2n + 0.25) - 0.5

计算出最小的满足条件的j就是答案

最后附上python代码：

```python
class Solution(object):
    def twoEggDrop(self, n):
        """
        :type n: int
        :rtype: int
        """

        res = int(sqrt((n * 2 + 0.25)) - 0.5)
        if res * (res + 1) < n + n:
            res += 1
        
        return res
```
