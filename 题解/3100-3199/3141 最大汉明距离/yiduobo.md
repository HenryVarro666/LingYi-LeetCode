---
title: "3141. 最大汉明距离"
aliases: ["yiduobo的每日leetcode 3141.最大汉明距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703037516"
zhihu_id: "703037516"
zhihu_title: "yiduobo的每日leetcode 3141.最大汉明距离"
question_id: "3141"
question: "最大汉明距离"
problem_url: "https://leetcode.cn/problems/maximum-hamming-distances/"
created: "2024-06-12T23:09:10+08:00"
updated: "2024-06-12T23:09:10+08:00"
upvotes: 1
comments: 0
---

# 3141. 最大汉明距离

> **[yiduobo的每日leetcode 3141.最大汉明距离](https://zhuanlan.zhihu.com/p/703037516) · 知乎 · 2024-06-12 · 赞同 1**
> 力扣：[3141. 最大汉明距离](https://leetcode.cn/problems/maximum-hamming-distances/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3141.最大汉明距离

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-hamming-distances/description/)

题目给出一个数组nums以及一个正整数m，nums[i]中的每个元素值都在0到2^m - 1之间，要求找出nums中每个元素nums[i]与其他所有元素汉明距离的最大值。

两个二进制整数的汉明距离指的是二者在对应位上二进制位不同的数量。

题目中m个取值范围可以达到17，而nums的长度则可以达到2^m，在极限情况下就是2^17 > 10^5，因此直接O(n^2)暴力循环计算显然是不行的。

对于汉明距离，一种常见的处理方法是将整数视为图中的节点，在仅有一个二进制位不同的整数对之间建立一条权重为1的边，这样一来就得到了一张权重都为1的无向图，而图中节点间的最短距离就是对应整数对的汉明距离。

不过本题要计算的是汉明距离的最大值，需要想办法进行转化。

对于处于0到2^m - 1之间的整数v，数值同样处于0到2^m - 1之间，且与v汉明距离最大的整数就是v的补码，即2^m - 1 - v，二者的二进制位上全都不同，因此汉明距离为m。

题目中需要找到nums中其他元素与每个nums\[i\]汉明距离的最大值，就可以转化为找出nums中其他元素与nums\[i\]补码的最小汉明距离，于是可以从nums中所有元素为起点进行bfs，计算0到2^m - 1之间所有数字距离这些元素的最短汉明距离，记为数组f。bfs完成后，对于nums\[i\]，其距离nums中其他元素的最大值，就可以通过m减去其补码到nums中其他元素的最小值，即m - f\[2^m - 1 - nums\[i\]\]得到。

最后附上python代码：

```python
class Solution(object):
    def maxHammingDistances(self, nums, m):
        """
        :type nums: List[int]
        :type m: int
        :rtype: List[int]
        """

        f = [None] * (1 << m)
        q = list(set(nums))
        for v in nums:
            f[v] = 0
        
        head, tail = 0, len(q)
        while head < tail:
            for x in q[head : tail]:
                for index in range(m):
                    y = x ^ (1 << index)
                    if f[y] is None:
                        f[y] = f[x] + 1
                        q.append(y)

            head, tail = tail, len(q)
        
        return [m - f[(1 << m) - 1 - v] for v in nums]
```
