---
title: "650. 只有两个键的键盘"
aliases: ["yiduobo的每日leetcode 650.只有两个键的键盘"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/278483773"
zhihu_id: "278483773"
zhihu_title: "yiduobo的每日leetcode 650.只有两个键的键盘"
question_id: "650"
question: "只有两个键的键盘"
problem_url: "https://leetcode.cn/problems/2-keys-keyboard/"
created: "2020-11-07T23:45:32+08:00"
updated: "2020-11-07T23:45:32+08:00"
upvotes: 1
comments: 0
---

# 650. 只有两个键的键盘

> **[yiduobo的每日leetcode 650.只有两个键的键盘](https://zhuanlan.zhihu.com/p/278483773) · 知乎 · 2020-11-07 · 赞同 1**
> 力扣：[650. 只有两个键的键盘](https://leetcode.cn/problems/2-keys-keyboard/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

650.只有两个键的键盘

[力扣](https://leetcode-cn.com/problems/2-keys-keyboard/)

首先我们先寻找如何快速进行倍增。

设我们当前有x个A，目标是将其倍增到kx个A，那么此时我们可以选择复制这x个A，然后粘贴k - 1次，即一共进行k次操作将x变为kx。若此时的k是合数，那么设k \= pq，若我们直接复制这x个A，那么需要pq次操作。另一种做法是先复制x个A，然后粘贴p - 1次，此时用了p次操作得到px个A，然后再复制这px个A，粘贴q - 1次，此时用了q次操作得到了kx个A，那么总共是使用p + q次操作。

由于k是合数，那么必然有pq >\= p + q，于是现在的思路就是对n进行质因数分解，不妨设

n \= p1 \* p2 \* p3 \* ... \* pm

那么总共需要p1 + p2 + ... + pm次操作

最后附上python代码：

```python
class Solution(object):
    def minSteps(self, n):
        """
        :type n: int
        :rtype: int
        """

        res = 0
        x = 2
        while n > 1:
            while n % x == 0:
                res += x
                n /= x
            x += 1

        return res
```
