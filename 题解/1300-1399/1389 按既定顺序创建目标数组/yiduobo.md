---
title: "1389. 按既定顺序创建目标数组"
aliases: ["yiduobo的每日leetcode 1389.按既定顺序创建目标数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/403604153"
zhihu_id: "403604153"
zhihu_title: "yiduobo的每日leetcode 1389.按既定顺序创建目标数组"
question_id: "1389"
question: "按既定顺序创建目标数组"
problem_url: "https://leetcode.cn/problems/create-target-array-in-the-given-order/"
created: "2021-08-25T23:20:57+08:00"
updated: "2021-08-25T23:20:57+08:00"
upvotes: 1
comments: 0
---

# 1389. 按既定顺序创建目标数组

> **[yiduobo的每日leetcode 1389.按既定顺序创建目标数组](https://zhuanlan.zhihu.com/p/403604153) · 知乎 · 2021-08-25 · 赞同 1**
> 力扣：[1389. 按既定顺序创建目标数组](https://leetcode.cn/problems/create-target-array-in-the-given-order/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1389.按既定目标创建目标数组

[力扣](https://leetcode-cn.com/problems/create-target-array-in-the-given-order/)

正经做法应该是使用平衡二叉树，令将index作为key，数值作为value插入到平衡二叉树当中。不过题目数组的规模很小，我在这里直接使用的朴素算法。

最后附上python代码：

```python
class Solution(object):
    def createTargetArray(self, nums, index):
        """
        :type nums: List[int]
        :type index: List[int]
        :rtype: List[int]
        """

        res = []
        n = len(nums)
        for i in range(n):
            if i == index[i]:
                res.append(nums[i])
            else:
                res = res[:index[i]] + [nums[i]] + res[index[i]:]
        
        return res
```
