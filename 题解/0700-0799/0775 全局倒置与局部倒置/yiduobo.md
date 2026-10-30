---
title: "775. 全局倒置与局部倒置"
aliases: ["yiduobo的每日leetcode 775.全局倒置与局部倒置"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/339900609"
zhihu_id: "339900609"
zhihu_title: "yiduobo的每日leetcode 775.全局倒置与局部倒置"
question_id: "775"
question: "全局倒置与局部倒置"
problem_url: "https://leetcode.cn/problems/global-and-local-inversions/"
created: "2020-12-27T16:27:48+08:00"
updated: "2020-12-27T16:27:48+08:00"
upvotes: 0
comments: 0
---

# 775. 全局倒置与局部倒置

> **[yiduobo的每日leetcode 775.全局倒置与局部倒置](https://zhuanlan.zhihu.com/p/339900609) · 知乎 · 2020-12-27 · 赞同 0**
> 力扣：[775. 全局倒置与局部倒置](https://leetcode.cn/problems/global-and-local-inversions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

775.全局倒置与局部倒置

[力扣](https://leetcode-cn.com/problems/global-and-local-inversions/)

首先，所有满足局部倒置的数对必然也是全局倒置，那么要判断全局倒置是否等于局部倒置，那么实际上就是要求是否存在不连续的逆序对。

由于这里只需要判断有没有，而不需要求具体的数量，因此我们可以从头到尾进行扫描，对于当前的nums[index]，若在nums[0]到nums[index - 2]之间的最大值大于nums[index]，那么就存在不连续的逆序对。对于这个最大值，可以在扫描过程中跟着维护。

最后附上python代码：

```python
class Solution(object):
    def isIdealPermutation(self, A):
        """
        :type A: List[int]
        :rtype: bool
        """

        max_num = 0
        for index in range(2, len(A)):
            max_num = max(max_num, A[index - 2])
            if max_num > A[index]:
                return False

        return True
```
