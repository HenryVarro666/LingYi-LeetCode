---
title: "873. 最长的斐波那契子序列的长度"
aliases: ["yiduobo的每日leetcode 873.最长的斐波那契子序列的长度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350432170"
zhihu_id: "350432170"
zhihu_title: "yiduobo的每日leetcode 873.最长的斐波那契子序列的长度"
question_id: "873"
question: "最长的斐波那契子序列的长度"
problem_url: "https://leetcode.cn/problems/length-of-longest-fibonacci-subsequence/"
created: "2021-02-13T17:08:40+08:00"
updated: "2021-02-13T17:08:40+08:00"
upvotes: 0
comments: 0
---

# 873. 最长的斐波那契子序列的长度

> **[yiduobo的每日leetcode 873.最长的斐波那契子序列的长度](https://zhuanlan.zhihu.com/p/350432170) · 知乎 · 2021-02-13 · 赞同 0**
> 力扣：[873. 最长的斐波那契子序列的长度](https://leetcode.cn/problems/length-of-longest-fibonacci-subsequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

873.最长的斐波那契子序列的长度

[力扣](https://leetcode-cn.com/problems/length-of-longest-fibonacci-subsequence/)

没有想到什么特别好的处理方法，我的做法是直接枚举数列的头两项，然后向后扩展，同时利用哈希表来判断当前项是否出现在arr当中，若存在则继续向后扩展并判断否则停止扩展并更新答案。

最后附上python代码：

```python
class Solution(object):
    def lenLongestFibSubseq(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        num_set = set(arr)
        n = len(arr)
        res = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                a, b = arr[i], arr[j]
                cnt = 0
                while a + b in num_set:
                    a, b = b, a + b
                    cnt += 1
                if cnt > 0:
                    res = max(res, cnt + 2)
        
        return res
```
