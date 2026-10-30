---
title: "1899. 合并若干三元组以形成目标三元组"
aliases: ["yiduobo的每日leetcode 1899.合并若干三元组以形成目标三元组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/480358495"
zhihu_id: "480358495"
zhihu_title: "yiduobo的每日leetcode 1899.合并若干三元组以形成目标三元组"
question_id: "1899"
question: "合并若干三元组以形成目标三元组"
problem_url: "https://leetcode.cn/problems/merge-triplets-to-form-target-triplet/"
difficulty: "Medium"
rating: 1636
created: "2022-03-13T21:18:56+08:00"
updated: "2022-03-13T21:18:56+08:00"
upvotes: 0
comments: 0
---

# 1899. 合并若干三元组以形成目标三元组

> **[yiduobo的每日leetcode 1899.合并若干三元组以形成目标三元组](https://zhuanlan.zhihu.com/p/480358495) · 知乎 · 2022-03-13 · 赞同 0**
> 力扣：[1899. 合并若干三元组以形成目标三元组](https://leetcode.cn/problems/merge-triplets-to-form-target-triplet/) · Medium · 灵茶山艾府：[判断满足要求的三元组各部分是否出现过](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1899.合并若干三元组以形成目标三元组

[力扣](https://leetcode-cn.com/problems/merge-triplets-to-form-target-triplet/)

题目使用一个三元组来更新另三元组时，取的都是较大值，这也就意味着如果某个三元组在其中一个维度上的值大于target中对应维度的值，那么就不能使用这个三元组来更新其他三元组。

而对于其他可用的三元组，如果其中某一维的值等于target中对应维度的值，那么通过这个三元组就能满足这一维，于是可以一趟遍历，对于可用的三元组判断三个维度是否可以被满足。

遍历完成后若三个维度都可以被满足，那么答案就是true，否则就是false。

最后附上python代码：

```python
class Solution(object):
    def mergeTriplets(self, triplets, target):
        """
        :type triplets: List[List[int]]
        :type target: List[int]
        :rtype: bool
        """

        flag1 = flag2 = flag3 = False;

        for x, y, z in triplets:
            if x == target[0] and y <= target[1] and z <= target[2]:
                flag1 = True
            if x <= target[0] and y == target[1] and z <= target[2]:
                flag2 = True
            if x <= target[0] and y <= target[1] and z == target[2]:
                flag3 = True
        
        return flag1 and flag2 and flag3
```
