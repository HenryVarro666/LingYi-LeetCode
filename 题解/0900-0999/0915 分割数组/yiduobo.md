---
title: "915. 分割数组"
aliases: ["yiduobo的每日leetcode 915.分割数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/355081767"
zhihu_id: "355081767"
zhihu_title: "yiduobo的每日leetcode 915.分割数组"
question_id: "915"
question: "分割数组"
problem_url: "https://leetcode.cn/problems/partition-array-into-disjoint-intervals/"
created: "2021-03-06T16:22:24+08:00"
updated: "2021-03-06T16:22:24+08:00"
upvotes: 0
comments: 0
---

# 915. 分割数组

> **[yiduobo的每日leetcode 915.分割数组](https://zhuanlan.zhihu.com/p/355081767) · 知乎 · 2021-03-06 · 赞同 0**
> 力扣：[915. 分割数组](https://leetcode.cn/problems/partition-array-into-disjoint-intervals/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

915.分割数组

[力扣](https://leetcode-cn.com/problems/partition-array-into-disjoint-intervals/)

题目要求将数组分成前后两个部分，且前面这个部分的每个数都要小于等于后面这个部分的每个数。这个条件可以简化为前面这个部分的最大值小于等于后面这个部分的最小值，也就是最大前缀以及最小后缀。这两个值可以通过正反两趟扫描求解出来。

求解完成后，就只需要从0开始向后枚举分割点，判断前面部分的最大值是否小于等于后面部分的最小值即可。

最后附上python代码：

```python
class Solution(object):
    def partitionDisjoint(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        max_list = [A[0]]
        for num in A[1:]:
            max_list.append(max(max_list[-1], num))
        
        min_list = [A[-1]]
        for num in A[::-1][1:]:
            min_list.append(min(min_list[-1], num))
        
        min_list.reverse()

        res = 0
        while max_list[res] > min_list[res + 1]:
            res += 1
        
        return res + 1
```
