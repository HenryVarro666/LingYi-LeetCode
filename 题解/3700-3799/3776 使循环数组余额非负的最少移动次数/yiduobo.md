---
title: "3776. 使循环数组余额非负的最少移动次数"
aliases: ["yiduobo的每日leetcode 3776.使循环数组余额非负的最少移动次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1984014909143549129"
zhihu_id: "1984014909143549129"
zhihu_title: "yiduobo的每日leetcode 3776.使循环数组余额非负的最少移动次数"
question_id: "3776"
question: "使循环数组余额非负的最少移动次数"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-balance-circular-array/"
difficulty: "Medium"
rating: 1740
created: "2025-12-17T01:48:37+08:00"
updated: "2025-12-17T01:48:41+08:00"
upvotes: 1
comments: 0
---

# 3776. 使循环数组余额非负的最少移动次数

> **[yiduobo的每日leetcode 3776.使循环数组余额非负的最少移动次数](https://zhuanlan.zhihu.com/p/1984014909143549129) · 知乎 · 2025-12-17 · 赞同 1**
> 力扣：[3776. 使循环数组余额非负的最少移动次数](https://leetcode.cn/problems/minimum-moves-to-balance-circular-array/) · Medium · 灵茶山艾府：[贪心，从近到远，O(1) 空间写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3776.使循环数组余额非负的最少移动次数

[3776. 使循环数组余额非负的最少移动次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-moves-to-balance-circular-array/description/)

题目给出一个长度为n的环形数组balance，其中balance[index]是第index个人的净余额。初始状态下，只有至多只有一个人的balance为负。

在一次移动中，一个人可以将正好1单位的余额转移给左边或者右边的邻居。

问至少需要多少次移动才能使得所有人的余额都非负。若无法实现，则返回-1。

首先考虑边界情况。

若balance中没有负数，那么就无需进行任何操作，此时的答案为0。

若balance之和为负数，说明负的那个人负得太多了，其他人即使全部给这个人还是负的，此时的答案为-1。

接下来考虑一般情况。

由于只有一个人余额为负，那么为了使得移动的次数最少，就应该尽可能先移动与其距离最近的人的余额。

不妨设余额为负的这个人在数组中的下标为p，那么对于p，首先就应该先移动左右两侧相邻的两个人的余额，然后是左右两侧距离为2的两个人的余额，以此类推，直到这个人的余额非负为止。于是可以使用两个指针left和right指向接下来移动余额的人的下标，然后left和right先移动余额，若移动完之后依然为负，则让left和right分别向左右两侧移动。需要注意的是，由于数组是环形数组，因此left和right的初始值应该是(p - 1 + n) % n以及(p + 1) % n，而在每次移动时，left都应该变为(left - 1 + n) % n，right则变为(right + 1) % n。

对于当前的left和right，先判断balance[left]与balance[right]之后是否足够填balance[p]，如果足够，那么移动的代价就是-balance[p]乘以p到这两个位置的距离；若不够，则需要将left和right的余额都给p，此时的代价为balance[left] + balance[right]之和，再乘以p到这两个为止的距离，接下来还需要将balance[p]加上这两个数之和，再将left和right分别向左右移动。

最后附上python代码：

```python
class Solution(object):
    def minMoves(self, balance):
        """
        :type balance: List[int]
        :rtype: int
        """
        

        if sum(balance) < 0:
            return -1
        
        p = 0
        n = len(balance)
        while p < n and balance[p] >= 0:
            p += 1
        
        if p == n:
            return 0
        
        left = (p - 1 + n) % n
        right = (p + 1) % n

        v = -balance[p]
        dis = 1
        res = 0
        while v:
            if balance[left] + balance[right] >= v:
                res += v * dis
                break
            else:
                res += (balance[left] + balance[right]) * dis
                v -= balance[left]
                v -= balance[right]
                left = (left - 1 + n) % n
                right = (right + 1) % n
                dis += 1
        
        return res
```
