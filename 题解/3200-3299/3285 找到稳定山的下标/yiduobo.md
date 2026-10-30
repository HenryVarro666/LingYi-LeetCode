---
title: "3285. 找到稳定山的下标"
aliases: ["yiduobo的每日leetcode 3285.找到稳定山的下标"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/842359235"
zhihu_id: "842359235"
zhihu_title: "yiduobo的每日leetcode 3285.找到稳定山的下标"
question_id: "3285"
question: "找到稳定山的下标"
problem_url: "https://leetcode.cn/problems/find-indices-of-stable-mountains/"
difficulty: "Easy"
created: "2024-10-06T22:05:42+08:00"
updated: "2024-10-06T22:05:42+08:00"
upvotes: 0
comments: 0
---

# 3285. 找到稳定山的下标

> **[yiduobo的每日leetcode 3285.找到稳定山的下标](https://zhuanlan.zhihu.com/p/842359235) · 知乎 · 2024-10-06 · 赞同 0**
> 力扣：[3285. 找到稳定山的下标](https://leetcode.cn/problems/find-indices-of-stable-mountains/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3285.找到稳定山的下标

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-indices-of-stable-mountains/description/)

题目给出一个长度为n的整数数组height，表示有n座山排在一起，其中第i座山的高度为height[i]。另外给出一个阈值threshold，对于某座下标大于0的山，若其左侧的山的高度大于threshold，那么就称这座山为稳定的。问哪些山是稳定的。

直接按照题目要求，从下标1开始向后一趟遍历模拟计算就行了：对于当前遍历到的第index座山，若height[index] > threshold，那么就将index加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def stableMountains(self, height, threshold):
        """
        :type height: List[int]
        :type threshold: int
        :rtype: List[int]
        """

        res = []
        for index in range(1, len(height)):
            if height[index - 1] > threshold:
                res.append(index)

        return res
```
