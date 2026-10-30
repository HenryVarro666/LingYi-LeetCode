---
title: "3499. 操作后最大活跃区段数I"
aliases: ["yiduobo的每日leetcode 3499.操作后最大活跃区段数I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1899630240860448154"
zhihu_id: "1899630240860448154"
zhihu_title: "yiduobo的每日leetcode 3499.操作后最大活跃区段数I"
question_id: "3499"
question: "操作后最大活跃区段数 I"
problem_url: "https://leetcode.cn/problems/maximize-active-section-with-trade-i/"
difficulty: "Medium"
rating: 1729
created: "2025-04-29T22:17:20+08:00"
updated: "2025-04-29T22:17:20+08:00"
upvotes: 0
comments: 0
---

# 3499. 操作后最大活跃区段数I

> **[yiduobo的每日leetcode 3499.操作后最大活跃区段数I](https://zhuanlan.zhihu.com/p/1899630240860448154) · 知乎 · 2025-04-29 · 赞同 0**
> 力扣：[3499. 操作后最大活跃区段数 I](https://leetcode.cn/problems/maximize-active-section-with-trade-i/) · Medium · 灵茶山艾府：[一次遍历，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3499.操作后最大活跃区段数I

[3499. 操作后最大活跃区段数 I - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-active-section-with-trade-i/description/)

题目给出一个长度为n的二进制字符串s，其中'1'表示一个活跃区段，'0'则表示一个非活跃区段。

现在可以执行至多一次操作来最大化s中的活跃区段数目。在一次操作中，可以将一个被'0'包围的连续'1'全部变为'0'，再将一个被'1'包围的连续'0'全部变为'1'。

问最终可以得到的s中的最大活跃区段数。

需要注意，在处理时需要在s的两侧加上'1'，即t \= '1' + s + '1'，但是两侧的'1'不影响最终的计数。

题目中的操作可以认为是将s中被连续1分割的两段连续的0都变为1。为了使得s中最终的1数量最多，在这里就应该选择数量最多的两段连续的0，因此在这里就可以先通过一趟遍历，将s中连续的1和0都分离出来,，在这个过程中记录1的总数res，并使用数组intervals记录所有连续0的起点和终点。接下来只需对intervals进行一趟遍历，找出其中最大的相邻区间长度和length，将length累加到res中即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxActiveSectionsAfterTrade(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        n = len(s)
        intervals = []
        p = 0
        res = n
        while p < n:
            while p < n and s[p] == '1':
                p += 1
            
            if p == n:
                break
            
            q = p + 1
            while q < n and s[q] == '0':
                q += 1
            
            intervals.append((p, q - 1))
            res -= q - p
            p = q
        
        length = 0
        for index in range(1, len(intervals)):
            length = max(length, intervals[index][1] - intervals[index][0] + 1 + intervals[index - 1][1] - intervals[index - 1][0] + 1)
        
        return res + length
```
