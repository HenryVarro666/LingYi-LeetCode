---
title: "2110. 股票平滑下跌阶段的数目"
aliases: ["yiduobo的每日leetcode 2110.股票平滑下跌阶段的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/523726126"
zhihu_id: "523726126"
zhihu_title: "yiduobo的每日leetcode 2110.股票平滑下跌阶段的数目"
question_id: "2110"
question: "股票平滑下跌阶段的数目"
problem_url: "https://leetcode.cn/problems/number-of-smooth-descent-periods-of-a-stock/"
difficulty: "Medium"
rating: 1408
created: "2022-06-02T21:02:54+08:00"
updated: "2022-06-02T21:02:54+08:00"
upvotes: 0
comments: 0
---

# 2110. 股票平滑下跌阶段的数目

> **[yiduobo的每日leetcode 2110.股票平滑下跌阶段的数目](https://zhuanlan.zhihu.com/p/523726126) · 知乎 · 2022-06-02 · 赞同 0**
> 力扣：[2110. 股票平滑下跌阶段的数目](https://leetcode.cn/problems/number-of-smooth-descent-periods-of-a-stock/) · Medium · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2110.股票平滑下跌截断的数目

<https://leetcode.cn/problems/number-of-smooth-descent-periods-of-a-stock/>

动态规划的题目。令f[i]表示以prices[i]结尾的平滑下跌阶段的数目，那么：

1、首先是边界情况，当i \= 0时显然有f[0] \= 1

2、接下来一般情况。对于f[i]：

2-1）若满足prices[i] \= prices[i - 1] - 1，那么可以在所有以prices[i - 1]结尾的平滑下跌阶段的基础上，将prices[i]添加到末尾形成以prices[i]结尾的平滑下跌阶段。除此之外，prices[i]单独拎出来也是合法的平滑下跌阶段，那么就有f[i] \= f[i - 1] + 1

2-2）若不满足prices[i] \= prices[i - 1] - 1，那么就只能把prices[i]单独拎出来，那么就有f[i] \= 1

一趟遍历，求解所有的f[i]并累加到答案中即可。

另外，在这里f[i]只与f[i - 1]有关，因此可以省去数组，采用变量迭代的方式计算每一轮的f值。

最后附上python代码：

```python
class Solution(object):
    def getDescentPeriods(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """

        n = len(prices)
        res = 1
        now = 1
        for index in range(1, n):
            if prices[index] == prices[index - 1] - 1:
                now += 1
            else:
                now = 1
            
            res += now

        return res
```
