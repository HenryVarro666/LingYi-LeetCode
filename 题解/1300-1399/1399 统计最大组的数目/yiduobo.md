---
title: "1399. 统计最大组的数目"
aliases: ["yiduobo的每日leetcode 1399.统计最大组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/enumeration", "leetcode/bao-li", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/404594315"
zhihu_id: "404594315"
zhihu_title: "yiduobo的每日leetcode 1399.统计最大组的数目"
question_id: "1399"
question: "统计最大组的数目"
problem_url: "https://leetcode.cn/problems/count-largest-group/"
difficulty: "Easy"
created: "2021-08-28T21:35:13+08:00"
updated: "2021-08-28T21:35:13+08:00"
upvotes: 0
comments: 0
---

# 1399. 统计最大组的数目

> **[yiduobo的每日leetcode 1399.统计最大组的数目](https://zhuanlan.zhihu.com/p/404594315) · 知乎 · 2021-08-28 · 赞同 0**
> 力扣：[1399. 统计最大组的数目](https://leetcode.cn/problems/count-largest-group/) · Easy · 灵茶山艾府：[两种方法：暴力枚举 / 数位 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1399.统计最大组的数目

[力扣](https://leetcode-cn.com/problems/count-largest-group/)

对于每个数字，计算其各位上的和，然后使用哈希表来储存每个数值和出现的次数，接下来对于这些次数，选择其中的最大值，并统计这个最大值出现的数目，即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def countLargestGroup(self, n):
        """
        :type n: int
        :rtype: int
        """

        s_dict = {}
        for index in range(1, n + 1):
            now = index
            s = 0
            while now:
                s += now % 10
                now /= 10

            s_dict[s] = s_dict.get(s, 0) + 1
        
        res = 0
        now_cnt = 0
        for cnt in s_dict.values():
            if cnt > now_cnt:
                res = 1
                now_cnt = cnt
            elif cnt == now_cnt:
                res += 1
            
        return res
```
