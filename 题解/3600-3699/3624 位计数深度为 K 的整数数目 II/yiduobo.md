---
title: "3624. 位计数深度为K的整数数目II"
aliases: ["yiduobo的每日leetcode 3624.位计数深度为K的整数数目II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/binary-indexed-tree", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1945163846777025186"
zhihu_id: "1945163846777025186"
zhihu_title: "yiduobo的每日leetcode 3624.位计数深度为K的整数数目II"
question_id: "3624"
question: "位计数深度为 K 的整数数目 II"
problem_url: "https://leetcode.cn/problems/number-of-integers-with-popcount-depth-equal-to-k-ii/"
difficulty: "Hard"
rating: 2086
created: "2025-08-30T17:04:14+08:00"
updated: "2025-08-30T17:04:14+08:00"
upvotes: 1
comments: 0
---

# 3624. 位计数深度为K的整数数目II

> **[yiduobo的每日leetcode 3624.位计数深度为K的整数数目II](https://zhuanlan.zhihu.com/p/1945163846777025186) · 知乎 · 2025-08-30 · 赞同 1**
> 力扣：[3624. 位计数深度为 K 的整数数目 II](https://leetcode.cn/problems/number-of-integers-with-popcount-depth-equal-to-k-ii/) · Hard · 灵茶山艾府：[6 个树状数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3624.位计数深度为K的整数数目II

[3624. 位计数深度为 K 的整数数目 II - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-integers-with-popcount-depth-equal-to-k-ii/description/)

对于任意正整数x，题目定义以下序列：

p[0] \= x

p[index + 1] \= popcount(p[index])，这里的popcount(y)表示的是y的二进制表示中1的数目。

这个序列最终会到达值1，而x的位计数深度则定义为使得p[index] \= 1的最小整数index。

例如对于x \= 7(二进制表示为111)，得到的序列为7(111) -> 3(11) -> 2(10) -> 1，因此7的位计数深度为3。

现在给出一个二维数组queries，其中的每个查询可能是以下两种类型之一：

[1, l, r, k]，表示要求计算在区间[l, r]中位计数深度等于k的元素数目，其中k小于等于5。

[2, index, val]，表示将nums[index]修改为val。

要求返回所有查询1的结果。

首先，对于查询区间[l, r]中满足条件的元素数目，可以转化为查询前缀[0, r]中满足条件的元素数目，减去前缀[0, l - 1]中满足条件的元素数目。另一方面，由于k不超过5，那么在这里完全可以对k从0到5这6种情况，每种情况都使用单独的数据结构来进行处理。又由于题目中还存在修改操作，那么结合起前缀运算，在这里使用6个树状数组来进行处理是比较合适的。

具体来说，可以先对nums进行一趟遍历，将其中的元素替换为其对应的位计数深度，同时将其对应的下标加入到位计数深度对应的树状数组中。接下来对于每种查询操作，若是第一种，则查询k对应的树状数组中前缀[1, r + 1]之间的元素数目与前缀[1, l]之间的元素数目之差。需要注意因为使用的是树状数组，所以下标必须从1开始，而原始数组中的下标需要往后推一位。而对于第二种操作，则只需先从原始的树状数组中移除对应的下标，然后计算新元素的位计数深度，将下标添加到对应的树状数组中并更新nums即可。

最后附上python代码：

```python
class Solution(object):
    def popcountDepth(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(nums)
        f = [[0] * (n + 1) for _ in range(6)]
        
        def add(k, x, delta):
            while x <= n:
                f[k][x] += delta
                x += x & -x

        def get(k, x):
            cnt = 0
            while x > 0:
                cnt += f[k][x]
                x -= x & -x
            return cnt

        for index, v in enumerate(nums):
            step = 0
            while v > 1:
                step += 1
                cnt = 0
                while v:
                    if v % 2 == 1:
                        cnt += 1
                    v //= 2
                v = cnt
            nums[index] = step
            add(step, index + 1, 1)

        res = []
        for q in queries:
            if q[0] == 1:
                res.append(get(q[3], q[2] + 1) - get(q[3], q[1]))
            else:
                add(nums[q[1]], q[1] + 1, -1)
                step = 0
                v = q[2]
                while v > 1:
                    step += 1
                    cnt = 0
                    while v:
                        if v % 2 == 1:
                            cnt += 1
                        v //= 2
                    v = cnt
                add(step, q[1] + 1, 1)
                nums[q[1]] = step
        
        return res
```
