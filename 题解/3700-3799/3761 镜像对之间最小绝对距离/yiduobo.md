---
title: "3761. 镜像对之间最小绝对距离"
aliases: ["yiduobo的每日leetcode 3761.镜像对之间最小绝对距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1978554517206356410"
zhihu_id: "1978554517206356410"
zhihu_title: "yiduobo的每日leetcode 3761.镜像对之间最小绝对距离"
question_id: "3761"
question: "镜像对之间最小绝对距离"
problem_url: "https://leetcode.cn/problems/minimum-absolute-distance-between-mirror-pairs/"
difficulty: "Medium"
rating: 1669
created: "2025-12-01T20:53:43+08:00"
updated: "2025-12-01T20:53:46+08:00"
upvotes: 2
comments: 0
---

# 3761. 镜像对之间最小绝对距离

> **[yiduobo的每日leetcode 3761.镜像对之间最小绝对距离](https://zhuanlan.zhihu.com/p/1978554517206356410) · 知乎 · 2025-12-01 · 赞同 2**
> 力扣：[3761. 镜像对之间最小绝对距离](https://leetcode.cn/problems/minimum-absolute-distance-between-mirror-pairs/) · Medium · 灵茶山艾府：[枚举右，维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3761.镜像对之间最小绝对距离

[3761. 镜像对之间最小绝对距离 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-absolute-distance-between-mirror-pairs/description/)

题目给出一个整数数组nums。

定义镜像对为一组下标对(i, j)，满足0 \<\= i \< j \< nums.length，且reverse(nums[i])与nums[j]相等。其中reverse(x)表示将整数x的数字反转后形成的整数。反转会忽略前导零，例如reverse(120) \= 21。

要求找出所有镜像对之间绝对距离的最小值，若不存在，则返回-1。

题目定义的镜像对是左侧下标i对应的元素反转后，与右侧下标j对应的元素相同，也就是说对于nums中的所有下标index，需要找出0到index - 1之间，满足reverse(nums[p]) \= nums[index]的最大的下标p，然后使用index - p更新答案。

于是可以一趟遍历，使用哈希表last记录前缀中每种元素反转后最后一次出现的位置。对于当前遍历到的index，先使用index - last\[nums\[index\]\]更新答案，然后将last\[reverse(nums\[index\])\]更新为index即可。

最后附上python代码：

```python
class Solution(object):
    def minMirrorPairDistance(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        last = {}
        res = -1
        for index, v in enumerate(nums):
            if v in last and (res == -1 or res > index - last[v]):
                res = index - last[v]

            r = 0
            while v:
                r = r * 10 + v % 10
                v //= 10
            last[r] = index
        
        return res
```
