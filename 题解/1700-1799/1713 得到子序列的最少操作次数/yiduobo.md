---
title: "1713. 得到子序列的最少操作次数"
aliases: ["yiduobo的每日leetcode 1713.得到子序列的最少操作次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/450065042"
zhihu_id: "450065042"
zhihu_title: "yiduobo的每日leetcode 1713.得到子序列的最少操作次数"
question_id: "1713"
question: "得到子序列的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-a-subsequence/"
created: "2021-12-26T19:04:23+08:00"
updated: "2021-12-26T19:04:23+08:00"
upvotes: 1
comments: 0
---

# 1713. 得到子序列的最少操作次数

> **[yiduobo的每日leetcode 1713.得到子序列的最少操作次数](https://zhuanlan.zhihu.com/p/450065042) · 知乎 · 2021-12-26 · 赞同 1**
> 力扣：[1713. 得到子序列的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-a-subsequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1713.得到子序列的最少操作次数

[力扣](https://leetcode-cn.com/problems/minimum-operations-to-make-a-subsequence/)

设target的长度为m，arr的长度为n。如果不考虑数据规模的话，可以使用动态规划先求出target和arr的最长公共子序列的长度l，然后m - l就是最终答案。

求解最长公共子序列的算法时间复杂度为O(mn)，在题目给出的数据规模下显然是不行的，必须想办法进行优化。注意到题目中给出了一个限制，target中的数互不相同，那么肯定是从这里想办法。

对于最长公共子序列中的两个数x \= target[p1] \= arr[p2]，y \= target[q1] \= arr[q2]，若p1 \< q1，那么就必然有p2 \< q2，反过来若p2 \< q2，那么p1 \< q1也成立。

由于target中的数互不相同，也就意味着target中的数与其在target中的位置是一一对应的。不妨记target中的每个数x在target中的位置为pos[x]，带入反过来的式子，就有

若p2 \< q2，那么pos[x] \< pos[y]

更进一步的，将x \= arr[p2]，y \= arr[q2]带入这个式子，就有

若p2 \< q2，那么pos\[arr\[p2\]\] \< pos\[arr\[q2\]\]

如果将其推广到整个最长公共子序列，那么对于最长公共子序列\[arr\[l_0\], arr\[l_1\], ..., arr\[l_k\]\]，就有

pos\[arr\[l_0\]\] \< pos\[arr\[l_1\]\] \< ... \< pos\[arr\[l_k\]\]

为了使得这个式子最长，那么就相当于在pos\[arr\[\*\]\]这个数组上求解最长上升子序列。

以样例2进行说明。

首先根据target[6, 4, 8, 1, 3, 2]得到pos，具体为

pos[6] \= 0

pos[4] \= 1

pos[8] \= 2

pos[1] \= 3

pos[3] \= 4

pos[2] \= 5

此时target和arr[4, 7, 6, 2, 3, 8, 6, 1]的最长公共子序列为[6, 8, 1]

如果将arr全部用pos进行替代，那么将得到[1, None, 0, 5, 4, 2, 0, 3]。这里的None表示这个数字并未在pos中出现，那么其也必然不可能属于最长公共子序列中，可以直接将其排除，那么最终得到的数组为[1, 0, 5, 4, 2, 0, 3]。对这个数组求最长上升子序列，得到的是[0, 2, 3]，对应的就是最长公共子序列[6, 8, 1]了。

对于最长上升子序列这个问题，是存在O(nlog(n))的贪心算法的，至此时间复杂度上的问题就解决了。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, target, arr):
        """
        :type target: List[int]
        :type arr: List[int]
        :rtype: int
        """

        pos_dict = {}
        for index, num in enumerate(target):
            pos_dict[num] = index

        f = []
        for num in arr:
            if num in pos_dict:
                pos = pos_dict[num]
                if not f or pos > f[-1]:
                    f.append(pos)
                else:
                    l = 0
                    r = len(f) - 1
                    while l < r:
                        mid = (l + r) >> 1
                        if f[mid] < pos:
                            l = mid + 1
                        else:
                            r = mid
                    
                    f[l] = pos
        
        return len(target) - len(f)
```
