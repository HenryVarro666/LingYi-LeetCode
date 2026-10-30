---
title: "832. 翻转图像"
aliases: ["yiduobo的每日leetcode 832.翻转图像"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/345276803"
zhihu_id: "345276803"
zhihu_title: "yiduobo的每日leetcode 832.翻转图像"
question_id: "832"
question: "翻转图像"
problem_url: "https://leetcode.cn/problems/flipping-an-image/"
created: "2021-01-23T16:21:02+08:00"
updated: "2021-01-23T16:21:02+08:00"
upvotes: 0
comments: 0
---

# 832. 翻转图像

> **[yiduobo的每日leetcode 832.翻转图像](https://zhuanlan.zhihu.com/p/345276803) · 知乎 · 2021-01-23 · 赞同 0**
> 力扣：[832. 翻转图像](https://leetcode.cn/problems/flipping-an-image/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

832.翻转图像

[力扣](https://leetcode-cn.com/problems/flipping-an-image/)

比较基础的题目。逐行遍历矩阵A，对于A中的每行，首先在答案矩阵中新起一行，然后从后往前一趟扫描A中的当前行，将1减去当前值加入到答案矩阵中新加入这一行的末尾即可。

最后附上python代码：

```python
class Solution(object):
    def flipAndInvertImage(self, A):
        """
        :type A: List[List[int]]
        :rtype: List[List[int]]
        """

        res = []
        for line in A:
            res.append([])
            for index in range(len(line) - 1, -1, -1):
                res[-1].append(1 - line[index])
        
        return res
```
