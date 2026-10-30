---
title: "1822. 数组元素积的符号"
aliases: ["yiduobo的每日leetcode 1822.数组元素积的符号"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/466393777"
zhihu_id: "466393777"
zhihu_title: "yiduobo的每日leetcode 1822.数组元素积的符号"
question_id: "1822"
question: "数组元素积的符号"
problem_url: "https://leetcode.cn/problems/sign-of-the-product-of-an-array/"
created: "2022-02-11T22:06:20+08:00"
updated: "2022-02-11T22:06:20+08:00"
upvotes: 0
comments: 0
---

# 1822. 数组元素积的符号

> **[yiduobo的每日leetcode 1822.数组元素积的符号](https://zhuanlan.zhihu.com/p/466393777) · 知乎 · 2022-02-11 · 赞同 0**
> 力扣：[1822. 数组元素积的符号](https://leetcode.cn/problems/sign-of-the-product-of-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1822.数组元素积的符号

[力扣](https://leetcode-cn.com/problems/sign-of-the-product-of-an-array/)

由于题目并不关心最终结果的大小，而只需要知道最终符号，因此可以直接一趟遍历，在过程中计算最终的符号。需要注意的是，若遍历过程中遇到了0，那么最终答案为0。

最后附上python代码：

```python
class Solution(object):
    def arraySign(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 1
        for num in nums:
            if num == 0:
                return 0
            if num < 0:
                res = -res
        
        return res
```
