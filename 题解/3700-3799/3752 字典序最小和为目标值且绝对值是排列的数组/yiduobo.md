---
title: "3752. 字典序最小和为目标值且绝对值是排列的数组"
aliases: ["yiduobo的每日leetcode 3752.字典序最小和为目标值且绝对值是排列的数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/two-pointers", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1976036920267134094"
zhihu_id: "1976036920267134094"
zhihu_title: "yiduobo的每日leetcode 3752.字典序最小和为目标值且绝对值是排列的数组"
question_id: "3752"
question: "字典序最小和为目标值且绝对值是排列的数组"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-negated-permutation-that-sums-to-target/"
difficulty: "Medium"
rating: 1827
created: "2025-11-24T19:09:03+08:00"
updated: "2025-11-24T19:09:04+08:00"
upvotes: 1
comments: 0
---

# 3752. 字典序最小和为目标值且绝对值是排列的数组

> **[yiduobo的每日leetcode 3752.字典序最小和为目标值且绝对值是排列的数组](https://zhuanlan.zhihu.com/p/1976036920267134094) · 知乎 · 2025-11-24 · 赞同 1**
> 力扣：[3752. 字典序最小和为目标值且绝对值是排列的数组](https://leetcode.cn/problems/lexicographically-smallest-negated-permutation-that-sums-to-target/) · Medium · 灵茶山艾府：[字典序贪心 + 可行性证明，O(n) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3752.字典序最小和为目标值且绝对值是排列的数组

[3752. 字典序最小和为目标值且绝对值是排列的数组 - 力扣（LeetCode）](https://leetcode.cn/problems/lexicographically-smallest-negated-permutation-that-sums-to-target/description/)

题目给出一个正整数n以及一个整数target，要求返回一个大小为n的字典序最小的整数数组，其元素之和等于target，同时其元素的绝对值组成一个大小为n的排列。若不存在，则返回一个空数组。

首先，当1到n全部取正数时，数组之和s \= (1 + n) \* n // 2，而当1到n全部取负数时，数组之和则为-s，也就是说，若target \< -s，或者target > s，答案必然为空。

接下来，可以将问题转化成一开始排列中所有元素全部为正，需要将其中部分元素取相反数，使得数组之和从s变为target。由于一个元素x取反后将变为-x，相当于从s中减去x \* 2，因此无论如何操作，最终数组元素之和必然与s的奇偶性相同。也就是说如果target与s的奇偶性不同，那么答案也为空。

另一方面，为了使得最终答案的字典序最小，在这里就应该在满足最终数组之和等于target的前提下，优先让较大的数取相反数，然后将所有的负数按从小到大的顺序放在答案的头部，将其他元素按照从小到大的顺序放在答案的尾部，这样一来才能使得字典序最小。

不妨记diff \= s - target，那么问题就转化成了从1到n中找出一些元素，这些元素之和恰好等于diff // 2。这是一个典型的背包问题，但是由于候选集是1到n，同时最终答案有应该尽量先取较大的元素，那么在这里有一种基于贪心的处理方法：

不妨设当前需要从1到v之间取若干个元素，使这些元素之和等于diff，那么当diff >\= v时，可以先取v，然后将问题转化为从1到v - 1之间取若干个元素，使这些元素之和等于diff - v；反之，当diff \< v时，由于目前1到v中的所有元素都可以取用，因此直接取值为diff的元素就行了。

这样一来，不仅可以使得取出的元素之和等于diff，同时取出元素的字典序也是最大的，取反后就得到了最小的字典序。

最后附上python代码：

```python
class Solution(object):
    def lexSmallestNegatedPerm(self, n, target):
        """
        :type n: int
        :type target: int
        :rtype: List[int]
        """
        
        s = (1 + n) * n // 2
        if target < -s or target > s:
            return []
        
        diff = s - target
        if diff % 2 == 1:
            return []
        
        diff //= 2
        part1 = []
        part2 = []
        for v in range(n, 0, -1):
            if diff >= v:
                part1.append(-v)
                diff -= v
            else:
                part2.append(v)
        
        return part1 + part2[::-1]
```
