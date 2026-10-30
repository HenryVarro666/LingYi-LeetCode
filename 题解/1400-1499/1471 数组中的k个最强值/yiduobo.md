---
title: "1471. 数组中的k个最强值"
aliases: ["yiduobo的每日leetcode 1471.数组中的k个最强值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/414336968"
zhihu_id: "414336968"
zhihu_title: "yiduobo的每日leetcode 1471.数组中的k个最强值"
question_id: "1471"
question: "数组中的k个最强值"
problem_url: "https://leetcode.cn/problems/the-k-strongest-values-in-an-array/"
created: "2021-09-26T23:16:54+08:00"
updated: "2021-09-26T23:16:54+08:00"
upvotes: 0
comments: 0
---

# 1471. 数组中的k个最强值

> **[yiduobo的每日leetcode 1471.数组中的k个最强值](https://zhuanlan.zhihu.com/p/414336968) · 知乎 · 2021-09-26 · 赞同 0**
> 力扣：[1471. 数组中的k个最强值](https://leetcode.cn/problems/the-k-strongest-values-in-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1471.数组中的k个最强值

[力扣](https://leetcode-cn.com/problems/the-k-strongest-values-in-an-array/)

首先，自然是先将数组进行排序并找出中位数m。

接下来分析题目给出的关于强的定义，可以发现越强的数其绝对值与m的距离就越远，也就是说此时的最强值必然是数组的最大值或者最小值之一。恰好现在数组已经完成排序，那么最强值必然就出现在数组的头部或者尾部。

当选出最强值之后，次强值必然是剩下数中的头部或者尾部。更进一步的，若每一轮都选出当前的最强值并将其从数组中移除，那么每一轮的最强值都会出现在数组中剩余数的头部或者尾部，于是可以使用双指针从两侧开始向中间扫描，每一轮都比较两个指针指向的数的前强弱程度，选择较强的那一个加入到答案中并将对应的指针向中间移动，直到找出k个值为止。

最后附上python代码：

```python
class Solution(object):
    def getStrongest(self, arr, k):
        """
        :type arr: List[int]
        :type k: int
        :rtype: List[int]
        """

        sorted_arr = sorted(arr)
        l = 0
        r = len(sorted_arr) - 1
        m = sorted_arr[r / 2]
        res = []
        while l <= r:
            if abs(sorted_arr[l] - m) > abs(sorted_arr[r] - m):
                res.append(sorted_arr[l])
                l += 1
            else:
                res.append(sorted_arr[r])
                r -= 1
        
            if len(res) == k:
                break

        return res
```
