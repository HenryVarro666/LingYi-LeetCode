---
title: "1566. 重复至少K次且长度为M的模式"
aliases: ["yiduobo的每日leetcode 1566.重复至少K次且长度为M的模式"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426988118"
zhihu_id: "426988118"
zhihu_title: "yiduobo的每日leetcode 1566.重复至少K次且长度为M的模式"
question_id: "1566"
question: "重复至少K次且长度为M的模式"
problem_url: "https://leetcode.cn/problems/detect-pattern-of-length-m-repeated-k-or-more-times/"
created: "2021-10-31T18:38:07+08:00"
updated: "2021-10-31T18:38:07+08:00"
upvotes: 0
comments: 0
---

# 1566. 重复至少K次且长度为M的模式

> **[yiduobo的每日leetcode 1566.重复至少K次且长度为M的模式](https://zhuanlan.zhihu.com/p/426988118) · 知乎 · 2021-10-31 · 赞同 0**
> 力扣：[1566. 重复至少K次且长度为M的模式](https://leetcode.cn/problems/detect-pattern-of-length-m-repeated-k-or-more-times/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1566.重复至少K次且长度为M的模式

[力扣](https://leetcode-cn.com/problems/detect-pattern-of-length-m-repeated-k-or-more-times/)

感觉可能可以用字符串相关的数据结构例如后缀数组来做，不过这里n、m、k的规模都很小，因此我直接使用的暴力法，枚举模式的起始位置，然后逐位进行检测。

最后附上python代码：

```python
class Solution(object):
    def containsPattern(self, arr, m, k):
        """
        :type arr: List[int]
        :type m: int
        :type k: int
        :rtype: bool
        """

        n = len(arr)
        for index in range(n):
            if index + m * k - 1 >= n:
                return False

            flag = True
            for i in range(m):
                now = arr[index + i]
                for j in range(1, k):
                    next = arr[index + i + m * j]
                    if now != next:
                        flag = False
                        break
                
                if not flag:
                    break
            
            if flag:
                return True
```
