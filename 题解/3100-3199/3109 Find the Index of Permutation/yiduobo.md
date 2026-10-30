---
title: "3109. Find the Index of Permutation"
aliases: ["yiduobo的每日leetcode 3109.Find the Index of Permutation"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/700602606"
zhihu_id: "700602606"
zhihu_title: "yiduobo的每日leetcode 3109.Find the Index of Permutation"
question_id: "3109"
question: "Find the Index of Permutation"
problem_url: "https://leetcode.cn/problems/find-the-index-of-permutation/"
created: "2024-05-29T23:41:00+08:00"
updated: "2024-05-29T23:41:00+08:00"
upvotes: 1
comments: 0
---

# 3109. Find the Index of Permutation

> **[yiduobo的每日leetcode 3109.Find the Index of Permutation](https://zhuanlan.zhihu.com/p/700602606) · 知乎 · 2024-05-29 · 赞同 1**
> 力扣：[3109. Find the Index of Permutation](https://leetcode.cn/problems/find-the-index-of-permutation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3109.Find the Index of Permutation

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-index-of-permutation/description/)

题目给出一个由1到n组成的排列perm，问这个排列在所有由1到n组成的排列中排名第几。

对于这个问题，有一种经典的算法叫做康托展开，其思路也很直观。对于由m个不同数字组成的排列，一共有m!种不同的排列，那么对于其中以第k小的数为开头的排列，以第1小都按第k - 1小的数为开头组成的排列的排名都会在这个排列前面，而以这些数为开头的排列的数量就是(k - 1) \* (m - 1)!个，其中(m - 1)!是因为剩下的m - 1个数可以构成(m - 1)!个不同的排列，因此一共有(k - 1) \* (m - 1)!个排列在以第k小的数为开头的排列之前。

根据这个结论，就可以对perm进行一趟遍历，对于当前遍历到的perm[index]，首先找出后续有多少个元素小于perm[index]，不妨记为k，那么此时就只需将k \* (n - index - 1)!累加到答案中，然后继续向后遍历即可。

而对于找出后续的元素中小于等于perm\[index\]的个数这个问题，则有一种经典的转化方法，将问题视为对于一个下标从1开始的长度为n的数组arr，其中arr\[v\]等于1则表示剩余的数组还存在v，而等于0则表示不存在v了，那么对于原来要查询的小于perm\[index\]的数的个数，则可以认为是查询arr\[1\] + arr\[2\] + ... + arr\[perm\[index\] - 1\]\]的和为多少，查询完成后，perm\[index\]不再出现在后续的数组中，因此还需要将arr\[perm\[index\]\]置为0。这是一个非常标准的动态区间前缀和问题，可以使用树状数组高效地求解。

最后附上python代码：

```python
class Solution(object):
    def getPermutationIndex(self, perm):
        """
        :type perm: List[int]
        :rtype: int
        """
        
        fac = [1]
        mod = 10 ** 9 + 7
        n = len(perm)
        for index in range(1, n):
            fac.append(fac[-1] * index % mod)

        f = [0] * (n + 1)

        def add(x, delta):
            while x <= n:
                f[x] += delta
                x += x & -x
        
        def get(x):
            s = 0
            while x > 0:
                s += f[x]
                x -= x & -x
            return s

        for index in range(1, n + 1):
            add(index, 1)
        
        res = 0
        for index, v in enumerate(perm[:n - 1]):
            res = (res + get(v - 1) * fac[n - 1 - index]) % mod
            add(v, -1)
        
        return res
```
