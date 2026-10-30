---
title: "2975. 移除栅栏得到的正方形田地的最大面积"
aliases: ["yiduobo的每日leetcode 2975.移除栅栏得到的正方形田地的最大面积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/enumeration", "leetcode/sorting", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692024372"
zhihu_id: "692024372"
zhihu_title: "yiduobo的每日leetcode 2975.移除栅栏得到的正方形田地的最大面积"
question_id: "2975"
question: "移除栅栏得到的正方形田地的最大面积"
problem_url: "https://leetcode.cn/problems/maximum-square-area-by-removing-fences-from-a-field/"
difficulty: "Medium"
created: "2024-04-12T01:41:57+08:00"
updated: "2024-04-12T01:41:57+08:00"
upvotes: 1
comments: 0
---

# 2975. 移除栅栏得到的正方形田地的最大面积

> **[yiduobo的每日leetcode 2975.移除栅栏得到的正方形田地的最大面积](https://zhuanlan.zhihu.com/p/692024372) · 知乎 · 2024-04-12 · 赞同 1**
> 力扣：[2975. 移除栅栏得到的正方形田地的最大面积](https://leetcode.cn/problems/maximum-square-area-by-removing-fences-from-a-field/) · Medium · 灵茶山艾府：[暴力枚举（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2975.移除栅栏得到的正方形田地的最大面积

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-square-area-by-removing-fences-from-a-field/description/)

本题与之前的2943题很像，不过本题是在空白的网格上给出了一些横杠和竖杠，问移除掉一些横杠和竖杠之后可以得到的最大正方形。

与之前相同，由于本题中水平和竖直方向也是互不影响的，因此可以分别找出水平和竖直方向上所有可以得到的连续空白值，然后找出最大的在两个方向上都出现过的连续空白值即可。

而对于单个方向上的空白值求解，则可以直接枚举所有的横杠或者竖杠对，计算差值。另外，需要注意本题网格的外框，也就是水平方向上的1和m，竖直方向上的1和n也是可以使用的。

最后附上python代码：

```python
class Solution(object):
    def maximizeSquareArea(self, m, n, hFences, vFences):
        """
        :type m: int
        :type n: int
        :type hFences: List[int]
        :type vFences: List[int]
        :rtype: int
        """

        def generate(fences, bound):
            fences = [1] + sorted(fences) + [bound]
            length_set = set()
            for i in range(len(fences) - 1):
                for j in range(i + 1, len(fences)):
                    length_set.add(fences[j] - fences[i])
            return length_set

        h_set = generate(hFences, m)
        v_set = generate(vFences, n)

        res = -1
        for x in h_set:
            if x in v_set:
                res = max(res, x * x)
        
        if res > 0:
            res %= 10 ** 9 + 7
        return res
```
