---
title: "2593. 标记所有元素后数组的分数"
aliases: ["yiduobo的每日leetcode 2593.标记所有元素后数组的分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/643691645"
zhihu_id: "643691645"
zhihu_title: "yiduobo的每日leetcode 2593.标记所有元素后数组的分数"
question_id: "2593"
question: "标记所有元素后数组的分数"
problem_url: "https://leetcode.cn/problems/find-score-of-an-array-after-marking-all-elements/"
difficulty: "Medium"
created: "2023-07-15T02:33:01+08:00"
updated: "2023-07-15T02:33:01+08:00"
upvotes: 0
comments: 0
---

# 2593. 标记所有元素后数组的分数

> **[yiduobo的每日leetcode 2593.标记所有元素后数组的分数](https://zhuanlan.zhihu.com/p/643691645) · 知乎 · 2023-07-15 · 赞同 0**
> 力扣：[2593. 标记所有元素后数组的分数](https://leetcode.cn/problems/find-score-of-an-array-after-marking-all-elements/) · Medium · 灵茶山艾府：[两种做法：从 O(nlogn) 到 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2593.标记所有元素后数组的分数

[力扣](https://leetcode.cn/problems/find-score-of-an-array-after-marking-all-elements/)

由于题目中的标记操作最多只需要标记三个位置，可以认为是O(1)的操作，因此可以直接模拟题目描述的操作。

首先将数组以数值为第一关键字，下标为第二关键字从小到大进行排序，然后一趟遍历，使用数组vis记录下标的使用情况。对于当前遍历到的数对(index, v)，若vis[index]为false，那么就将v累加到答案，同时将vis[index]、vis[index - 1]以及vis[index + 1]这三个位置标记为true。在这里需要注意判断index - 1和index + 1是否越界。

最后附上python代码：

```python
class Solution(object):
    def findScore(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        vis = [False] * n
        res = 0
        for index, v in sorted(enumerate(nums), key=lambda d:(d[1], d[0])):
            if not vis[index]:
                res += v
                vis[index] = True
                if index > 0:
                    vis[index - 1] = True
                if index < n - 1:
                    vis[index + 1] = True
        
        return res
```
