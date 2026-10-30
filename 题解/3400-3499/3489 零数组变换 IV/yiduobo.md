---
title: "3489. 零数组变换IV"
aliases: ["yiduobo的每日leetcode 3489.零数组变换IV"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/38750414487"
zhihu_id: "38750414487"
zhihu_title: "yiduobo的每日leetcode 3489.零数组变换IV"
question_id: "3489"
question: "零数组变换 IV"
problem_url: "https://leetcode.cn/problems/zero-array-transformation-iv/"
difficulty: "Medium"
rating: 2068
created: "2025-04-25T22:05:03+08:00"
updated: "2025-04-25T22:05:03+08:00"
upvotes: 0
comments: 0
---

# 3489. 零数组变换IV

> **[yiduobo的每日leetcode 3489.零数组变换IV](https://zhuanlan.zhihu.com/p/38750414487) · 知乎 · 2025-04-25 · 赞同 0**
> 力扣：[3489. 零数组变换 IV](https://leetcode.cn/problems/zero-array-transformation-iv/) · Medium · 灵茶山艾府：[两种方法：0-1 背包 / 二分答案+多重背包（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3489.零数组变换IV

[3489. 零数组变换 IV - 力扣（LeetCode）](https://leetcode.cn/problems/zero-array-transformation-iv/)

题目给出一个长度为n的整数数组nums，nums的长度不超过10。另外给出一个二维数组queries，其中queries\[i\] \= \[l\[i\], r\[i\], val\[i\]\]。

对于每个查询queries\[i\]，可以在下标范围\[l\[i\], r\[i\]\]中选择一个下标子集，将这些下标对应的元素减去正好val\[i\]。

现在要求找出一个最小的k，使得在执行queries中的前k个查询后，nums将全变为0。

之前3356题的变形，但是本题的操作变成了减去正好val，具体的做法也完全不同了。由于nums的长度不超过10，那么一个自然的想法就是分别针对nums中的每个元素计算最小的k，这些k中的最大值即为最终答案。

对于nums[index]，题目要求找出一个最小的k，使得可以从queries[0]到queries[k]中选出若干组query，这些query对应的left和right要包含index，同时这些query对应的val相加需要刚好等于target。对于从一些数中选出某些数相加刚好得到目标值这个问题，是动态规划问题中经典的背包问题。

于是可以令f[v]表示从当前这些queries中选出若干query能否凑出v，接下来只需遍历所有的queries，若当前query对应的left和right包含了index，就可以使用当前query对应的val来更新f，具体更新方式为从target到val倒序遍历，若f[x - val]为true，那么f[x]就可以更新为true，其含义也很直观，就是在之前选出的queries凑出的x - val的基础上选择当前的query，从而得到x。

若某一时刻f[target]为true，那么当前遍历的queries的下标即为当前的nums[index]对应的k，应该使用这个k更新最终答案。若f[target]始终都不为true，那么说明没法凑出当前的nums[index]，直接返回-1。

最后附上python代码：

```python
class Solution(object):
    def minZeroArray(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: int
        """
        
        res = 0
        for index, target in enumerate(nums):
            f = [False] * (target + 1)
            f[0] = True
            p = 0
            while p < len(queries) and not f[-1]:
                left, right, val = queries[p]
                p += 1
                if index < left or index > right:
                    continue
                
                for x in range(target, val - 1, -1):
                    if f[x - val]:
                        f[x] = True
            
            if not f[-1]:
                return -1

            res = max(res, p)
        
        return res
```
