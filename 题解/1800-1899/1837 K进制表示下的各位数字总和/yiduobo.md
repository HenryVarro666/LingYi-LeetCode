---
title: "1837. K进制表示下的各位数字总和"
aliases: ["yiduobo的每日leetcode 1837.K进制表示下的各位数字总和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/468868154"
zhihu_id: "468868154"
zhihu_title: "yiduobo的每日leetcode 1837.K进制表示下的各位数字总和"
question_id: "1837"
question: "K进制表示下的各位数字总和"
problem_url: "https://leetcode.cn/problems/sum-of-digits-in-base-k/"
created: "2022-02-17T23:15:47+08:00"
updated: "2022-02-17T23:15:47+08:00"
upvotes: 0
comments: 0
---

# 1837. K进制表示下的各位数字总和

> **[yiduobo的每日leetcode 1837.K进制表示下的各位数字总和](https://zhuanlan.zhihu.com/p/468868154) · 知乎 · 2022-02-17 · 赞同 0**
> 力扣：[1837. K进制表示下的各位数字总和](https://leetcode.cn/problems/sum-of-digits-in-base-k/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1837.K进制表示下的各位数字总和

[力扣](https://leetcode-cn.com/problems/sum-of-digits-in-base-k/)

比较基础的题目，直接用取余法计算n的k进制表示，将这些余数累加起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def sumBase(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        res = 0
        while n:
            res += n % k
            n /= k
        
        return res
```
