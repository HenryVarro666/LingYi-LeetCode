---
title: "3577. 统计计算机解锁顺序排列数"
aliases: ["yiduobo的每日leetcode 3577.统计计算机解锁顺序排列数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/math", "leetcode/combinatorics", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1937505256532598888"
zhihu_id: "1937505256532598888"
zhihu_title: "yiduobo的每日leetcode 3577.统计计算机解锁顺序排列数"
question_id: "3577"
question: "统计计算机解锁顺序排列数"
problem_url: "https://leetcode.cn/problems/count-the-number-of-computer-unlocking-permutations/"
difficulty: "Medium"
rating: 1750
created: "2025-08-09T13:40:22+08:00"
updated: "2025-08-09T13:40:23+08:00"
upvotes: 1
comments: 0
---

# 3577. 统计计算机解锁顺序排列数

> **[yiduobo的每日leetcode 3577.统计计算机解锁顺序排列数](https://zhuanlan.zhihu.com/p/1937505256532598888) · 知乎 · 2025-08-09 · 赞同 1**
> 力扣：[3577. 统计计算机解锁顺序排列数](https://leetcode.cn/problems/count-the-number-of-computer-unlocking-permutations/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3577.统计计算机解锁顺序排列数

[3577. 统计计算机解锁顺序排列数 - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-computer-unlocking-permutations/description/)

题目给出一个长度为n的数组complexiy，表示有n台上锁的计算机，这些计算机的编号为0到n - 1，且每台计算机有一个唯一的密码，第index台计算机的密码复杂度为complexity[index]。

在最开始，编号为0的计算机密码已经解锁，并作为根节点。其他所有的计算机都必须通过它或者已经解锁的计算机来解锁，解锁的规则如下：

1、可以使用编号为j的计算机的密码解锁编号为i的计算机，其中j是任意小于i的整数，且满足complexity[j] \< complexity[i]

2、要解锁编号为i的计算机，必须事先解锁一个编号为j的计算机，满足j \< i且complexity[j] \< complexity[i]

问有多少种0到n - 1的排列方式，表示从编号为0的计算机开始解锁所有计算机的有效顺序。

观察题目中对于解锁规则的描述，可以发现，除了0号机以外，其他所有计算机都必须依靠一台编号和复杂度都更小的计算机来解锁。如果将所有计算机和其解锁时依赖的计算机之间连上一条边话，就可以得到一颗树，这棵树的每个节点值都大于其根节点的值，而整棵树的根节点为0号节点。换言之，0号机的复杂度必然是整棵树中最小的，也就是说树中所有计算机都可以直接通过0号机来解锁，而无法通过0号机解锁的计算机也无法通过其他计算机解锁。

基于上面这一点，只需一趟遍历，若存在复杂度大于等于complexity[0]的计算机，那么说明这台计算机无法解锁，最终答案为0，否则答案就是(n - 1)!，因为其他计算机都可以通过0号机来解锁，因此可以按照任意顺序来解锁，n - 1个数可以形成的排列为(n - 1)!

最后附上python代码：

```python
class Solution(object):
    def countPermutations(self, complexity):
        """
        :type complexity: List[int]
        :rtype: int
        """
        
        for v in complexity[1:]:
            if v <= complexity[0]:
                return 0
        
        res = 1
        mod = 10 ** 9 + 7
        for index in range(1, len(complexity)):
            res = res * index % mod
        return res
```
