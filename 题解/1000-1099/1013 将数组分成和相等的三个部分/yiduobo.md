---
title: "1013. 将数组分成和相等的三个部分"
aliases: ["yiduobo的每日leetcode 1013.将数组分成和相等的三个部分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/367526087"
zhihu_id: "367526087"
zhihu_title: "yiduobo的每日leetcode 1013.将数组分成和相等的三个部分"
question_id: "1013"
question: "将数组分成和相等的三个部分"
problem_url: "https://leetcode.cn/problems/partition-array-into-three-parts-with-equal-sum/"
created: "2021-04-24T20:08:15+08:00"
updated: "2021-04-24T20:08:15+08:00"
upvotes: 0
comments: 0
---

# 1013. 将数组分成和相等的三个部分

> **[yiduobo的每日leetcode 1013.将数组分成和相等的三个部分](https://zhuanlan.zhihu.com/p/367526087) · 知乎 · 2021-04-24 · 赞同 0**
> 力扣：[1013. 将数组分成和相等的三个部分](https://leetcode.cn/problems/partition-array-into-three-parts-with-equal-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1013.将数组分成和相等的三个部分

[力扣](https://leetcode-cn.com/problems/partition-array-into-three-parts-with-equal-sum/)

题目要求将数组分成和相等的三个部分，那么我们可以首先求出所有数的总和s，若s不是3的倍数，那么直接返回false，否则我们可以计算出每个部分的目标和target \= s / 3。

接下里，由于这里的每个部分必须是连续的，那么实际上就只需要求数组的前缀和prefix，若求解过程出现了prefix等于target以及prefix等于target \* 2的情况，且后者出现的位置不是数组末尾，并且与前者出现的位置也不同，那么就说明按照这两种情况出现的位置进行划分就可以得到和相等的三个部分，于是返回true。若遍历完成也没有找到上面所说合法的位置，那么返回false。

最后附上python代码：

```python
class Solution(object):
    def canThreePartsEqualSum(self, arr):
        """
        :type arr: List[int]
        :rtype: bool
        """

        s = sum(arr)
        if s % 3 != 0:
            return False

        target = s / 3
        prefix_s = 0
        flag = False
        for index, num in enumerate(arr):
            prefix_s += num
            if not flag:
                if prefix_s == target:
                    flag = True
            elif prefix_s == target + target and index != len(arr) - 1:
                return True
        
        return False
```
