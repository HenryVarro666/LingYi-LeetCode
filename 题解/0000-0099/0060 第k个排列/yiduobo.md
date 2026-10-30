---
title: "60. 第k个排列"
aliases: ["yiduobo的每日leetcode 60.第k个排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/129086910"
zhihu_id: "129086910"
zhihu_title: "yiduobo的每日leetcode 60.第k个排列"
question_id: "60"
question: "第k个排列"
problem_url: "https://leetcode.cn/problems/permutation-sequence/"
created: "2020-04-11T23:00:10+08:00"
updated: "2020-04-11T23:00:10+08:00"
upvotes: 0
comments: 0
---

# 60. 第k个排列

> **[yiduobo的每日leetcode 60.第k个排列](https://zhuanlan.zhihu.com/p/129086910) · 知乎 · 2020-04-11 · 赞同 0**
> 力扣：[60. 第k个排列](https://leetcode.cn/problems/permutation-sequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

60.第k个排列<https://leetcode-cn.com/problems/permutation-sequence/>

经典的排列组合问题，可以用康拓展开的方法来求解。

具体来说就是运用题目第一行给出的提示，n个元素的排列有n！种。那么以1开头的排列一共有(n - 1)！种，以2开头的也是(n - 1)！种，以此类推。于是，就有第1到(n - 1)！种排列都是以1开头的，第(n - 1)！+ 1到第(n - 1)！\* 2种排列都是以2开头的，以此类推。

因此，可以通过用k除以(n - 1)！来确定出第一位是哪个数字。需要注意的是，**这里得到的商代表的并不是当前这一位应该是多少，而是当前这一位在剩余数字中是第几小的**。

运用上面的方法找出第一位数之后，接下来的问题就变成了了n - 1个元素构成的第k mod (n - 1)！个排列是什么。只需如法炮制，一位一位往后找就行了。

最后附上python代码：

```python
class Solution(object):
    def getPermutation(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """

        factor_list = [1, 1, 2, 6, 24, 120, 720, 5040, 40320]
        candidate_list = [str(index) for index in range(1, n+1)]
        res = []
        
        k -= 1
        for pos in range(n - 1, 0, -1):
            offset = k / factor_list[pos]
            k %= factor_list[pos]
            res.append(str(candidate_list[offset]))
            for index in range(offset, pos):
                candidate_list[index] = candidate_list[index + 1]

        res.append(candidate_list[0])

        return ''.join(res)
```
