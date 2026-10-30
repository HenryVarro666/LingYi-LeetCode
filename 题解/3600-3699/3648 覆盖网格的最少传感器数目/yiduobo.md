---
title: "3648. 覆盖网格的最少传感器数目"
aliases: ["yiduobo的每日leetcode 3648.覆盖网格的最少传感器数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948174685163487479"
zhihu_id: "1948174685163487479"
zhihu_title: "yiduobo的每日leetcode 3648.覆盖网格的最少传感器数目"
question_id: "3648"
question: "覆盖网格的最少传感器数目"
problem_url: "https://leetcode.cn/problems/minimum-sensors-to-cover-grid/"
difficulty: "Medium"
rating: 1396
created: "2025-09-09T22:24:53+08:00"
updated: "2025-09-09T22:24:57+08:00"
upvotes: 0
comments: 0
---

# 3648. 覆盖网格的最少传感器数目

> **[yiduobo的每日leetcode 3648.覆盖网格的最少传感器数目](https://zhuanlan.zhihu.com/p/1948174685163487479) · 知乎 · 2025-09-09 · 赞同 0**
> 力扣：[3648. 覆盖网格的最少传感器数目](https://leetcode.cn/problems/minimum-sensors-to-cover-grid/) · Medium · 灵茶山艾府：[O(1) 数学公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3648.覆盖网格的最少传感器数目

[3648. 覆盖网格的最少传感器数目 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-sensors-to-cover-grid/description/)

题目给出一个n \* m的网格和一个整数k。一个放置在(r, c)的传感器可以覆盖所有与(r, c)的切比雪夫距离不超过k的单元格。两个单元格(r1, c1)与(r2, c2)之间的切比雪夫距离为max(|r1 - r2|, |c1 - c2|)。

问最少需要多少个传感器才能覆盖整个网格。

从题目中关于切比雪夫距离的描述来看，一个放置在(r, c)的传感器实际上可以覆盖住以(r, c)为中心的，边长为k \* 2 + 1的正方形，方便期间，在这里将边处记为x。由于是正方形，那么对于原始网格中边边角角的覆盖方式就比较明确了。

对于网格的左上角，最优的覆盖方式显然是在(k, k)处放置一个传感器，这样一来在覆盖了(0, 0)的同时，对于其他位置的覆盖程度也最大。基于这一点，最上面这一行的(0, 0)到(0, x - 1)就都被覆盖住了，而接下来如果要覆盖(0, x)，就应该在(k, x + k)处放置第二个传感器，以此类推，因此在第k行上，放置一共(m - 1) // x + 1个传感器，就可以覆盖住整个第0到第x - 1行。

接下来对于第x行开始的覆盖方法也是类似，一共有n列，因此需要这样排布置(n - 1) // x + 1次，那么最终答案就是每一行的传感器数量(m - 1) // x + 1，乘以需要排布的行数(n - 1) // x + 1。

最后附上python代码：

```python
class Solution(object):
    def minSensors(self, n, m, k):
        """
        :type n: int
        :type m: int
        :type k: int
        :rtype: int
        """
        
        x = k * 2 + 1
        return ((n - 1) // x + 1) * ((m - 1) // x + 1)
```
