---
title: "3694. 删除子字符串后的不同终点"
aliases: ["yiduobo的每日leetcode 3694.删除子字符串后的不同终点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1956115497843160789"
zhihu_id: "1956115497843160789"
zhihu_title: "yiduobo的每日leetcode 3694.删除子字符串后的不同终点"
question_id: "3694"
question: "删除子字符串后不同的终点"
problem_url: "https://leetcode.cn/problems/distinct-points-reachable-after-substring-removal/"
difficulty: "Medium"
rating: 1739
created: "2025-10-01T21:57:31+08:00"
updated: "2025-10-01T21:57:31+08:00"
upvotes: 0
comments: 0
---

# 3694. 删除子字符串后的不同终点

> **[yiduobo的每日leetcode 3694.删除子字符串后的不同终点](https://zhuanlan.zhihu.com/p/1956115497843160789) · 知乎 · 2025-10-01 · 赞同 0**
> 力扣：[3694. 删除子字符串后不同的终点](https://leetcode.cn/problems/distinct-points-reachable-after-substring-removal/) · Medium · 灵茶山艾府：[等价转换 + 定长滑动窗口 + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3694.删除子字符串后的不同终点

<https://leetcode.cn/problems/distinct-points-reachable-after-substring-removal/description/>

题目给出一个由'U'、'D'、'L'、'R'组成的字符串s，表示在无限二维平面上的移动。其中

'U'：表示从(x, y)移动到(x, y + 1)

'D'：表示从(x, y)移动到(x, y - 1)

'L'：表示从(x, y)移动到(x - 1, y)

'R'：表示从(x, y)移动到(x + 1, y)

另外给出一个正整数k，要求从s中移除一个长度恰好为k的子串，然后从(0, 0)开始，按顺序执行剩余的移动。问可能得到的不同最终坐标的数量。

从s中移除一个子串，就相当于在原始最终位置的基础上增加了一个偏移量。由于题目只需要找出最终可以到达的不同坐标数量，而不需要知道具体的坐标，因此不同偏移量的数量实际上就是可以到达的不同最终坐标数量。于是只需使用一个长度为k的滑动窗口从头开始向后滑动，计算窗口内下标的偏移量，并使用集合记录这些偏移量。滑动完成后，集合的大小即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def distinctPoints(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        
        def move(x, y, c, delta):
            if c == 'U':
                return x, y + delta
            elif c == 'D':
                return x, y - delta
            elif c == 'L':
                return x - delta, y
            else:
                return x + delta, y
        
        dx, dy = 0, 0
        for c in s[:k]:
            dx, dy = move(dx, dy, c, 1)
        vis = set([(dx, dy)])
        
        for index, c in enumerate(s[k:]):
            dx, dy = move(dx, dy, c, 1)
            dx, dy = move(dx, dy, s[index], -1)
            vis.add((dx, dy))
        
        return len(vis)
```
