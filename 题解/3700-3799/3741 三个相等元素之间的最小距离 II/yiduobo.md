---
title: "3740. 三个相等元素之间的最小距离I & 3741. 三个相等元素之间的最小距离II"
aliases: ["yiduobo的每日leetcode 3740.三个相等元素之间的最小距离I && 3741.三个相等元素之间的最小距离II", "3740. 三个相等元素之间的最小距离I", "3741. 三个相等元素之间的最小距离II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/medium", "leetcode/array"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1970888488711878048"
zhihu_id: "1970888488711878048"
zhihu_title: "yiduobo的每日leetcode 3740.三个相等元素之间的最小距离I && 3741.三个相等元素之间的最小距离II"
question_id: ["3740", "3741"]
question: ["三个相等元素之间的最小距离 I", "三个相等元素之间的最小距离 II"]
problem_url: ["https://leetcode.cn/problems/minimum-distance-between-three-equal-elements-i/", "https://leetcode.cn/problems/minimum-distance-between-three-equal-elements-ii/"]
difficulty: ["Easy", "Medium"]
created: "2025-11-10T21:45:04+08:00"
updated: "2025-11-10T21:45:11+08:00"
upvotes: 2
comments: 0
---

# 3740. 三个相等元素之间的最小距离I & 3741. 三个相等元素之间的最小距离II

> **[yiduobo的每日leetcode 3740.三个相等元素之间的最小距离I && 3741.三个相等元素之间的最小距离II](https://zhuanlan.zhihu.com/p/1970888488711878048) · 知乎 · 2025-11-10 · 赞同 2**
> 力扣：[3740. 三个相等元素之间的最小距离 I](https://leetcode.cn/problems/minimum-distance-between-three-equal-elements-i/) · Easy · 灵茶山艾府：[O(n) 做法（Python/Java/C++/Go）](../3740%20三个相等元素之间的最小距离%20I/灵茶山艾府.md)
> 力扣：[3741. 三个相等元素之间的最小距离 II](https://leetcode.cn/problems/minimum-distance-between-three-equal-elements-ii/) · Medium · 灵茶山艾府：[按照相同元素分组 / 记录上上一次的出现位置（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3740.三个相等元素之间的最小距离I

[3740. 三个相等元素之间的最小距离 I - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-distance-between-three-equal-elements-i/description/)

3741.三个相等元素之间的最小距离II

<https://leetcode.cn/problems/minimum-distance-between-three-equal-elements-ii/description/>

题目给出一个整数数组nums。

对于一个下标三元素(i, j, k)，若满足nums[i] \=\= nums[j] \=\= nums[k]，且i、j、k互不相同，那么就称其为有效三元组。

有效三元组的距离被定义为abs(i - j) + abs(j - k) + abs(k - i)，其中abs(x)表示x的绝对值。

要求找出nums中所有有效三元组的最小可能距离。若不存在有效三元组，则返回-1。

两题的一致，第二题的数据规模较大，nums的长度可达10^5。

由于i、j、k是等价的，因此在这里可以默认i \< j \< k。基于这一点，将三个绝对值拆开，就可以得到三元组的距离为j - i + k - j + k - i \= 2 \* (k - i)，即三元组中最左侧和最右侧距离的两倍。为了使得这个值最小，就应该让这两个元素离得尽可能近，也就是说最终答案必然出自于某个元素在nums中所有下标的列表中的三个连续下标。

于是只需使用两个哈希表p1和p2记录每种元素上一次和上上次出现的位置，接下来一趟遍历，对于当前位置index，不妨设其对应的元素为v，那么若p2[v]存在，就可以使用(index - p2[v]) \* 2来更新答案，然后使用p1[v]和index来更新p2[v]和p1[v]即可。

最后附上python代码：

```python
class Solution(object):
    def minimumDistance(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        p1 = {}
        p2 = {}
        res = -1

        for index, v in enumerate(nums):
            if p2.get(v, None) is not None:
                dis = (index - p2[v]) * 2
                if res == -1 or res > dis:
                    res = dis
            
            p2[v], p1[v] = p1.get(v, None), index
        
        return res
```
