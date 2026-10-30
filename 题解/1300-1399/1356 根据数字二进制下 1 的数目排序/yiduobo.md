---
title: "1356. 根据数字二进制下1的数目排序"
aliases: ["yiduobo的每日leetcode 1356.根据数字二进制下1的数目排序"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sorting", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/398462549"
zhihu_id: "398462549"
zhihu_title: "yiduobo的每日leetcode 1356.根据数字二进制下1的数目排序"
question_id: "1356"
question: "根据数字二进制下 1 的数目排序"
problem_url: "https://leetcode.cn/problems/sort-integers-by-the-number-of-1-bits/"
difficulty: "Easy"
rating: 1258
created: "2021-08-10T23:17:13+08:00"
updated: "2021-08-10T23:17:13+08:00"
upvotes: 1
comments: 0
---

# 1356. 根据数字二进制下1的数目排序

> **[yiduobo的每日leetcode 1356.根据数字二进制下1的数目排序](https://zhuanlan.zhihu.com/p/398462549) · 知乎 · 2021-08-10 · 赞同 1**
> 力扣：[1356. 根据数字二进制下 1 的数目排序](https://leetcode.cn/problems/sort-integers-by-the-number-of-1-bits/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1356.根据数字二进制下1的数目排序

[力扣](https://leetcode-cn.com/problems/sort-integers-by-the-number-of-1-bits/)

比较基础的题目，直接求出每个数二进制表示下1的数目，然后按照题意排序即可。

最后附上python代码：

```python
class Solution(object):
    def sortByBits(self, arr):
        """
        :type arr: List[int]
        :rtype: List[int]
        """

        cnt_list = []
        for num in arr:
            tmp = num
            cnt_list.append(0)
            while tmp:
                cnt_list[-1] += tmp % 2
                tmp /= 2
        
        return [x[0] for x in sorted(zip(arr, cnt_list), key=lambda d:(d[1], d[0]))]
```
