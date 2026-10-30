---
title: "3404. 统计特殊子序列的数目"
aliases: ["yiduobo的每日leetcode 3404.统计特殊子序列的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/enumeration", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/零-常用枚举技巧", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/31398261418"
zhihu_id: "31398261418"
zhihu_title: "yiduobo的每日leetcode 3404.统计特殊子序列的数目"
question_id: "3404"
question: "统计特殊子序列的数目"
problem_url: "https://leetcode.cn/problems/count-special-subsequences/"
difficulty: "Medium"
rating: 2445
created: "2025-03-19T22:19:30+08:00"
updated: "2025-03-19T22:19:30+08:00"
upvotes: 1
comments: 0
---

# 3404. 统计特殊子序列的数目

> **[yiduobo的每日leetcode 3404.统计特殊子序列的数目](https://zhuanlan.zhihu.com/p/31398261418) · 知乎 · 2025-03-19 · 赞同 1**
> 力扣：[3404. 统计特殊子序列的数目](https://leetcode.cn/problems/count-special-subsequences/) · Medium · 灵茶山艾府：[两种方法：前后缀分解 / 枚举右维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3404.统计特殊子序列的数目

[3404. 统计特殊子序列的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-special-subsequences/description/)

题目给出一个仅包含正整数的数组nums。特殊子序列指的是一个长度为4的子序列，用下标(p, q, r, s)来表示，并且满足q - p > 1，r - q > 1，s - r > 1，同时nums[p] \* nums[r] \= nums[q] \* nums[s]。

问nums中特殊子序列的数目。

对于这类下标有顺序要求的计数类问题，一种常见的做法是使用哈希表记录前缀中所有满足某种条件的下标对数量，然后枚举所有下标，一边使用哈希表更新答案，一边更新哈希表，先更新答案还是先更新哈希表则可以视具体问题而定。

回到本题。首先观察题目中给出的等式，发现两边的顺序是错开的，需要先进行变形。由于题目保证了nums中都是正整数，因此可以将等式变形为nums[p] / nums[q] \= nums[s] / nums[r]。

这样一来，等式左边就是靠前的两个位置p和q，右边则是靠后的r和s。到了这里就有了初步的思路，需要枚举右侧的s和r，使用哈希表统计左侧每种nums[p] / nums[q]出现的次数。

另一方面，由于哈希表记录的是当前遍历完成的前缀中的下标对，因此当r向后移动时，只需在之前哈希表的基础上额外考虑q \= r - 2的情况，也就是说枚举r时可以唯一确定本轮需要计算的q，接下来只要分别枚举p和s，先使用每一组nums[p] / nums[q]更新哈希表，然后对于每一组nums[s] / nums[r]，使用哈希表中出现的次数更新答案即可。

在具体实现上，由于题目中的除法是实数除法，为了能使用哈希表，因此需要先计算分子分母的最大公约数然后约分，以分子分母对为key的方式来使用哈希表。

最后附上python代码：

```python
class Solution(object):
    def numberOfSubsequences(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        prefix = {}
        res = 0
        for r in range(4, n - 2):
            q = r - 2
            for p in range(q - 1):
                x, y = nums[p], nums[q]
                g = gcd(x, y)
                x //= g
                y //= g
                key = (x, y)
                prefix[key] = prefix.get(key, 0) + 1
        
            for s in range(r + 2, n):
                x = nums[s]
                y = nums[r]
                g = gcd(x, y)
                x //= g
                y //= g
                key = (x, y)
                res += prefix.get(key, 0)
        
        return res
```
