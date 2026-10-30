---
title: "3187. 数组中的峰值"
aliases: ["yiduobo的每日leetcode 3187.数组中的峰值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706303253"
zhihu_id: "706303253"
zhihu_title: "yiduobo的每日leetcode 3187.数组中的峰值"
question_id: "3187"
question: "数组中的峰值"
problem_url: "https://leetcode.cn/problems/peaks-in-array/"
difficulty: "Hard"
rating: 2154
created: "2024-07-01T00:12:55+08:00"
updated: "2024-07-01T00:12:55+08:00"
upvotes: 1
comments: 0
---

# 3187. 数组中的峰值

> **[yiduobo的每日leetcode 3187.数组中的峰值](https://zhuanlan.zhihu.com/p/706303253) · 知乎 · 2024-07-01 · 赞同 1**
> 力扣：[3187. 数组中的峰值](https://leetcode.cn/problems/peaks-in-array/) · Hard · 灵茶山艾府：[树状数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3187.数组中的峰值

[. - 力扣（LeetCode）](https://leetcode.cn/problems/peaks-in-array/)

题目给出一个整数数组nums，对于nums中除了首尾元素之外的其他元素，若当前元素既大于其上一个元素，又大于其下一个元素，就称这个元素为峰值元素。

接下来给出一个二维数组queries，其中包含两种操作：

1、给出一组[l, r]，计算nums[l]到nums[r]之间峰值元素的数目

2、给出一组[index, val]，将nums[index]修改为val

要求返回所有查询1的结果

首先考虑第一种操作。

对于询问区间内满足条件的元素的个数这类问题，一种常见的转化思路是新开一个数组来将符合/不符合条件转化为1和0，然后通过加和来计算区间内满足条件的元素数量。

对于本题，令peek[index]表示nums[index]是否为峰值元素，若nums[index]是峰值元素，那么peek[index]就等于1，否则peek[index]就等于0。这样一来，nums[l]到nums[r]之间峰值元素的数目，就相当于peek[l]到peek[r]这一段的区间和，而对于区间和问题，则可以通过前缀和来高效计算。

由于peek的值是可能产生变化的，那么在这里就是一个动态的前缀和问题，可以使用树状数组求解。

接下来考虑第二种操作。

第二种操作则比较简单，只需实时更新nums[index]以及peek[index]，并计算当前的peek[index]与更新前的peek[index]之差，然后利用这个差值更新树状数组即可。

最后附上python代码：

```python
class Solution(object):
    def countOfPeaks(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(nums)
        peek = [0] * n
        f = [0] * (n + 1)

        def update(index):
            if index == 0 or index == n - 1:
                return
            
            new_val = 0
            if nums[index] > nums[index - 1] and nums[index] > nums[index + 1]:
                new_val = 1
            
            if peek[index] == new_val:
                return
            
            x = index + 1
            while x <= n:
                f[x] += new_val - peek[index]
                x += x & -x
            
            peek[index] = new_val

        def get(x):
            s = 0
            while x:
                s += f[x]
                x -= x & -x
            return s

        for index in range(1, n - 1):
            update(index)

        res = []
        for q in queries:
            if q[0] == 1:
                if q[1] + 1 <= q[2] - 1:
                    res.append(get(q[2]) - get(q[1] + 1))
                else:
                    res.append(0)
            else:
                nums[q[1]] = q[2]
                update(q[1])
                if q[1] > 0:
                    update(q[1] - 1)
                if q[1] < n - 1:
                    update(q[1] + 1)
        
        return res
```
