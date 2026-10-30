---
title: "1085. 最小元素各数位之和"
aliases: ["yiduobo的每日leetcode 1085.最小元素各数位之和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/608666811"
zhihu_id: "608666811"
zhihu_title: "yiduobo的每日leetcode 1085.最小元素各数位之和"
question_id: "1085"
question: "最小元素各数位之和"
problem_url: "https://leetcode.cn/problems/sum-of-digits-in-the-minimum-number/"
created: "2023-02-23T00:30:20+08:00"
updated: "2023-02-23T00:30:20+08:00"
upvotes: 0
comments: 0
---

# 1085. 最小元素各数位之和

> **[yiduobo的每日leetcode 1085.最小元素各数位之和](https://zhuanlan.zhihu.com/p/608666811) · 知乎 · 2023-02-23 · 赞同 0**
> 力扣：[1085. 最小元素各数位之和](https://leetcode.cn/problems/sum-of-digits-in-the-minimum-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1085.最小元素各数位之和

[力扣](https://leetcode.cn/problems/sum-of-digits-in-the-minimum-number/)

一趟遍历找出数组中的最小值，然后逐位分离个位数字并累加起来得到s，最后返回s + 1对2取模的结果即可。

最后附上python代码：

```python
class Solution(object):
    def sumOfDigits(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        mi = min(nums)
        s = 0
        while mi:
            s += mi % 10
            mi /= 10
        
        return (s + 1) % 2
```
