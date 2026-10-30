---
title: "3737. 统计主要元素子数组数目I & 3739. 统计主要元素子数组数目II"
aliases: ["yiduobo的每日leetcode 3737.统计主要元素子数组数目I && 3739.统计主要元素子数组数目II", "3737. 统计主要元素子数组数目I", "3739. 统计主要元素子数组数目II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/ordered-set", "leetcode/prefix-sum", "leetcode/hard", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1970880401045161320"
zhihu_id: "1970880401045161320"
zhihu_title: "yiduobo的每日leetcode 3737.统计主要元素子数组数目I && 3739.统计主要元素子数组数目II"
question_id: ["3737", "3739"]
question: ["统计主要元素子数组数目 I", "统计主要元素子数组数目 II"]
problem_url: ["https://leetcode.cn/problems/count-subarrays-with-majority-element-i/", "https://leetcode.cn/problems/count-subarrays-with-majority-element-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2090
created: "2025-11-09T16:00:47+08:00"
updated: "2025-11-09T16:01:05+08:00"
upvotes: 2
comments: 1
---

# 3737. 统计主要元素子数组数目I & 3739. 统计主要元素子数组数目II

> **[yiduobo的每日leetcode 3737.统计主要元素子数组数目I && 3739.统计主要元素子数组数目II](https://zhuanlan.zhihu.com/p/1970880401045161320) · 知乎 · 2025-11-09 · 赞同 2**
> 力扣：[3737. 统计主要元素子数组数目 I](https://leetcode.cn/problems/count-subarrays-with-majority-element-i/) · Medium · 灵茶山艾府：[O(n) 做法（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3739. 统计主要元素子数组数目 II](https://leetcode.cn/problems/count-subarrays-with-majority-element-ii/) · Hard · 灵茶山艾府：[枚举右维护左，O(n) 做法（Python/Java/C++/Go）](../3739%20统计主要元素子数组数目%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3737.统计主要元素子数组数目I

[3737. 统计主要元素子数组数目 I - 力扣（LeetCode）](https://leetcode.cn/problems/count-subarrays-with-majority-element-i/description/)

3739.统计主要元素子数组数目II

[3739. 统计主要元素子数组数目 II - 力扣（LeetCode）](https://leetcode.cn/problems/count-subarrays-with-majority-element-ii/description/)

题目给出一个整数数组nums以及一个整数target，要求找出nums中满足target是主要元素的子数组的数目。一个子数组的主要元素，指的是该元素在这个子数组中出现的次数严格大于子数组长度的一半。

两题的题设相同，第二题的数据规模较大，nums的长度可达10^5。

由于已经给出了指定的target，那么如果将nums中所有等于target的元素视为1，不等于target的元素视为-1，那么问题就转化成了给出一个1和-1组成的数组，问子数组和大于0的子数组数目。

之前遇到过类似的版本，是给出1和-1组成的数组，问子数组和恰好等于0的子数组数目，可以通过前缀和配合哈希表解决。

对于本题，同样是将区间和转化为前缀和之差，不过对于本题，需要计算的是对于每个前缀和s，其左侧所有小于s的前缀和的数目，因此在这里不能继续使用哈希表，而是需要使用树状数组来处理。

具体来说，使用一个变量s记录当前的前缀和，接下来对数组进行一趟遍历，若当前元素等于target，就将s加上1，否则将s减去1。接下来，通过树状数组查找之前出现过的，和小于等于s - 1的前缀的数目，将其累加到答案中，然后使用s更新树状数组即可。

最后附上python代码：

```python
class Solution(object):
    def countMajoritySubarrays(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        
        n = len(nums)
        f = [0] * (n + n + 2)
        s = 0
        res = 0

        def get(x):
            res = 0
            while x > 0:
                res += f[x]
                x -= x & -x
            return res
        
        def add(x):
            while x <= n + n + 1:
                f[x] += 1
                x += x & -x

        add(n + 1)
        for v in nums:
            if v == target:
                s += 1
            else:
                s -= 1
            
            res += get(s + n)
            add(s + n + 1)
        
        return res
```
