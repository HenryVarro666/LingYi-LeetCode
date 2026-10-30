---
title: "2913. 子数组不同元素数目的平方和I"
aliases: ["yiduobo的每日leetcode 2913.子数组不同元素数目的平方和I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/segment-tree"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664611066"
zhihu_id: "664611066"
zhihu_title: "yiduobo的每日leetcode 2913.子数组不同元素数目的平方和I"
question_id: "2913"
question: "子数组不同元素数目的平方和 I"
problem_url: "https://leetcode.cn/problems/subarrays-distinct-element-sum-of-squares-i/"
difficulty: "Easy"
created: "2023-11-02T02:08:33+08:00"
updated: "2023-11-02T02:08:35+08:00"
upvotes: 0
comments: 0
---

# 2913. 子数组不同元素数目的平方和I

> **[yiduobo的每日leetcode 2913.子数组不同元素数目的平方和I](https://zhuanlan.zhihu.com/p/664611066) · 知乎 · 2023-11-02 · 赞同 0**
> 力扣：[2913. 子数组不同元素数目的平方和 I](https://leetcode.cn/problems/subarrays-distinct-element-sum-of-squares-i/) · Easy · 灵茶山艾府：[O(nlogn) 线段树做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2913.子数组不同元素数目的平方和I

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/subarrays-distinct-element-sum-of-squares-i/)

题目的数据规模比较小，完全可以先枚举子数组的左边界i，然后从i开始向右逐步扩展子数组，同时使用一个集合记录当前子数组中的元素。接下来每一步只需将右边界对应的数加入到集合中，然后将集合中元素个数的平方累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def sumCounts(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        res = 0
        for i in range(n):
            num_set = set()
            for j in range(i, n):
                num_set.add(nums[j])
                res += len(num_set) ** 2
        
        return res
```
