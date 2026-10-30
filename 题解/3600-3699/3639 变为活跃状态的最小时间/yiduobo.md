---
title: "3639. 变为活跃状态的最小时间"
aliases: ["yiduobo的每日leetcode 3639.变为活跃状态的最小时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "leetcode/binary-search", "题单/二分算法", "题单/贪心算法", "题单/二分算法/二-二分答案", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1947425695996285391"
zhihu_id: "1947425695996285391"
zhihu_title: "yiduobo的每日leetcode 3639.变为活跃状态的最小时间"
question_id: "3639"
question: "变为活跃状态的最小时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-activate-string/"
difficulty: "Medium"
rating: 1853
created: "2025-09-05T23:21:41+08:00"
updated: "2025-09-05T23:21:41+08:00"
upvotes: 1
comments: 0
---

# 3639. 变为活跃状态的最小时间

> **[yiduobo的每日leetcode 3639.变为活跃状态的最小时间](https://zhuanlan.zhihu.com/p/1947425695996285391) · 知乎 · 2025-09-05 · 赞同 1**
> 力扣：[3639. 变为活跃状态的最小时间](https://leetcode.cn/problems/minimum-time-to-activate-string/) · Medium · 灵茶山艾府：[两种方法：二分答案 / 逆向思维+双向链表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3639.变为活跃的状态的最小时间

[3639. 变为活跃状态的最小时间 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-to-activate-string/description/)

题目给出一个长度为n的字符串s以及一个整数数组order，其中order是0到n - 1的一个排列。

从时间t \= 0开始，在每个时间点，都会将字符串s中下标为order[t]的字符替换为'\*'。

若一个子字符串中包含至少一个'\*'，则认为该子字符串有效。若字符串中的有效子串数量大于等于k，则认为该字符串是活跃字符串。问将s变为活跃的最小时间t，若无法让s变为活跃字符串，那么返回-1。

首先处理边界情况。对于一个长度为n的字符串，若其中的字符全都是星号，也就是说其所有子串都是有效子串，那么一共会有n \* (n + 1) // 2个子串。若这个值小于k，那么可以直接返回-1，否则必然存在某个时刻会使得s中有效子串的数量大于等于k。

接下来就需要想办法就算每个时刻有效子串的数量。

直接计算有效子串的数量是比较麻烦的，对于这类计算至少出现一次的问题，一种常见的处理方法是反过来计算，也就是计算一个星号都没有的子串的数量，然后使用子串的总数减去这个数量，就得到了有效子串的数量。对于一个星号都没有子串数量，则需要知道当前的s被星号分割成了每一段子串的长度，对于一段长度m的子串，可以贡献m个长度为1的非有效子串，m - 1个长度为2的非有效子串，...，1个长度为m的非有效字符串，一共是(m + 1) \* m // 2个非有效子串。将所有的非有效子串数量累加起来，然后使用字符串中子串的总数，也就是(n + 1) \* n // 2减去非有效字符串的数量，就得到了有效字符串的数量。

接下来的问题就是如何确定每一个时刻s被分割后的所有子串的长度。如果从区间的角度来看，问题就变成了一开始给出一个大区间[0, n - 1]，接下来每个时刻，都会对目前现有的一个区间进行分割。对于这个问题，可以使用平衡树记录现存的所有区间，但是比较麻烦。另一种处理方法就是再次反过来计算，即从一开始一个区间都没有，然后随着时间的往前推，一个个点被逐渐加回来，在这个过程中处理区间的新增以及合并。

具体来说，使用两个哈希表left和right分别记录每个下标所在区间的左边界以及右边界，接下来从时刻n - 1开始向回倒推。

对于当前的时间index，需要将order[index]所在的字符从星号变回原字符，另外这次变换可能连接以order[index] - 1为右边界的区间以及以order[index] + 1为左边界的区间，前提是这两个区间存在，因此在这里还要另起一个数组stars，其中stars[index]表示index这个下标当前是否为星号。

接下来对于order[index]，若stars[order[index] - 1]为false，说明order[index]将连接起左侧的区间，这个区间的左边界为left[order[index] - 1]，方便起见，在这里记为new_left。

同样的，若start[order[index] + 1]为false，说明order[index]将连接起右侧的区间，这个区间的右边界为right[order[index] + 1]，在这里记为new_right。

在加入order[index]后，原始的两个区间，也就是[new_left, order[index] - 1]以及[order[index + 1], new_right]将被合并成一个大区间[new_left, new_right]，此时只需基于这三个区间的长度，在之前有效区间数量的基础上，先加上两个短区间可以形成的非有效子串的数量，然后再减去大区间可以形成的非有效子串数量，就是当前时刻的有效区间数量了。

需要特别注意的是，对于下标order[index]，若order[index] - 1是星号，那么新区间的左边界就是order[index]自身，此时将new_left置为order[index]即可。同样的，若order[index] + 1是星号，那么将new_right置为order[index]即可。

计算完当前时刻的有效区间数量后，若其小于k，说明当前时刻即为最终答案，否则就需要将left\[new_right\]以及right\[new_left\]分别更新为new_left和new_right，并将starts\[order\[index\]\]置为false，然后将时间继续向前推。

最后附上python代码：

```python
class Solution(object):
    def minTime(self, s, order, k):
        """
        :type s: str
        :type order: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(s)
        activity = n * (n + 1) // 2
        if activity < k:
            return -1
        
        stars = [False] * n
        for index in order:
            stars[index] = True
        left = [None] * n
        right = [None] * n
        
        for index in range(len(order) - 1, -1, -1):
            o = order[index]
            if o > 0 and not stars[o - 1]:
                new_left = left[o - 1]
            else:
                new_left = o
            
            if o + 1 < n and not stars[o + 1]:
                new_right = right[o + 1]
            else:
                new_right = o
            
            activity += (o - new_left) * (o - new_left + 1) // 2
            activity += (new_right - o) * (new_right - o + 1) // 2
            activity -= (new_right - new_left + 1) * (new_right - new_left + 2) // 2
            right[new_left] = new_right
            left[new_right] = new_left
            stars[o] = False
            if activity < k:
                return index
```
