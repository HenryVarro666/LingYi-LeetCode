---
title: "1437. 是否所有1都至少相隔k个元素"
aliases: ["yiduobo的每日leetcode 1437.是否所有1都至少相隔k个元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/409580341"
zhihu_id: "409580341"
zhihu_title: "yiduobo的每日leetcode 1437.是否所有1都至少相隔k个元素"
question_id: "1437"
question: "是否所有 1 都至少相隔 k 个元素"
problem_url: "https://leetcode.cn/problems/check-if-all-1s-are-at-least-length-k-places-away/"
difficulty: "Easy"
created: "2021-09-12T16:57:52+08:00"
updated: "2021-09-12T16:57:52+08:00"
upvotes: 0
comments: 0
---

# 1437. 是否所有1都至少相隔k个元素

> **[yiduobo的每日leetcode 1437.是否所有1都至少相隔k个元素](https://zhuanlan.zhihu.com/p/409580341) · 知乎 · 2021-09-12 · 赞同 0**
> 力扣：[1437. 是否所有 1 都至少相隔 k 个元素](https://leetcode.cn/problems/check-if-all-1s-are-at-least-length-k-places-away/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1437.是否所有1都至少相隔k个元素

[力扣](https://leetcode-cn.com/problems/check-if-all-1s-are-at-least-length-k-places-away/)

直接一趟扫描，计算每个1距离上一个1出现的距离，若其中有小于k的，那么就返回false，否则返回true。

最后附上python代码：

```python
class Solution(object):
    def kLengthApart(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """

        cnt = k
        for index, num in enumerate(nums):
            if num == 1:
                if cnt < k:
                    return False
                cnt = 0
            else:
                cnt += 1
        
        return True
```
