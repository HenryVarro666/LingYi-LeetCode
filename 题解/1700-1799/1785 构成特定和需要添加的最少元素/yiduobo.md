---
title: "1785. 构成特定和需要添加的最少元素"
aliases: ["yiduobo的每日leetcode 1785.构成特定和需要添加的最少元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463060147"
zhihu_id: "463060147"
zhihu_title: "yiduobo的每日leetcode 1785.构成特定和需要添加的最少元素"
question_id: "1785"
question: "构成特定和需要添加的最少元素"
problem_url: "https://leetcode.cn/problems/minimum-elements-to-add-to-form-a-given-sum/"
created: "2022-01-29T21:46:11+08:00"
updated: "2022-01-29T21:46:11+08:00"
upvotes: 0
comments: 0
---

# 1785. 构成特定和需要添加的最少元素

> **[yiduobo的每日leetcode 1785.构成特定和需要添加的最少元素](https://zhuanlan.zhihu.com/p/463060147) · 知乎 · 2022-01-29 · 赞同 0**
> 力扣：[1785. 构成特定和需要添加的最少元素](https://leetcode.cn/problems/minimum-elements-to-add-to-form-a-given-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1785.构成特定和需要添加的最少元素

[力扣](https://leetcode-cn.com/problems/minimum-elements-to-add-to-form-a-given-sum/)

为了使得添加的元素最少，那么就应该顶着limit来添加数字，那么可以先计算出当前数组和与goal的差距delta，然后就可以用delta / limit计算出需要添加的数字个数。当然，若delta模limit不等于0，则还需要添加一个额外的数字。

最后附上python代码：

```python
class Solution(object):
    def minElements(self, nums, limit, goal):
        """
        :type nums: List[int]
        :type limit: int
        :type goal: int
        :rtype: int
        """

        delta = abs(sum(nums) - goal)
        res = delta / limit
        if delta % limit != 0:
            res += 1
        
        return res
```
