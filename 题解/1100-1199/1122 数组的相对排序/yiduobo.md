---
title: "1122. 数组的相对排序"
aliases: ["yiduobo的每日leetcode 1122.数组的相对排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/375863202"
zhihu_id: "375863202"
zhihu_title: "yiduobo的每日leetcode 1122.数组的相对排序"
question_id: "1122"
question: "数组的相对排序"
problem_url: "https://leetcode.cn/problems/relative-sort-array/"
created: "2021-05-27T22:46:46+08:00"
updated: "2021-05-27T22:46:46+08:00"
upvotes: 0
comments: 0
---

# 1122. 数组的相对排序

> **[yiduobo的每日leetcode 1122.数组的相对排序](https://zhuanlan.zhihu.com/p/375863202) · 知乎 · 2021-05-27 · 赞同 0**
> 力扣：[1122. 数组的相对排序](https://leetcode.cn/problems/relative-sort-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1122.数组的相对排序

[力扣](https://leetcode-cn.com/problems/relative-sort-array/)

题目要求将arr1按照arr2中的顺序为第一关键字，本身的数值大小为第二关键字进行排序，那么我们可以先建立起arr2中每个数字对当前下标的映射。设arr2的长度为l，那么这里面的l个数字就会分别与0到l - 1之间的数组形成映射，那么不在arr2中的数字，我们可以统一将其映射到l上。

接下来只需要执行一次sort，按照映射值为第一关键字，本身数值为第二关键字从小到大进行排序即可。

最后附上python代码：

```python
class Solution(object):
    def relativeSortArray(self, arr1, arr2):
        """
        :type arr1: List[int]
        :type arr2: List[int]
        :rtype: List[int]
        """

        p = {}
        l = len(arr2)
        for index, num in enumerate(arr2):
            p[num] = index
        
        arr1 = sorted(arr1, key=lambda d:(p.get(d, l), d))
        return arr1
```
