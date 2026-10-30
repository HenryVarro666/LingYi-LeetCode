---
title: "1151. 最少交换次数来组合所有的1"
aliases: ["yiduobo的每日leetcode 1151.最少交换次数来组合所有的1"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/610881708"
zhihu_id: "610881708"
zhihu_title: "yiduobo的每日leetcode 1151.最少交换次数来组合所有的1"
question_id: "1151"
question: "最少交换次数来组合所有的1"
problem_url: "https://leetcode.cn/problems/minimum-swaps-to-group-all-1s-together/"
created: "2023-03-02T23:17:43+08:00"
updated: "2023-03-02T23:17:43+08:00"
upvotes: 1
comments: 0
---

# 1151. 最少交换次数来组合所有的1

> **[yiduobo的每日leetcode 1151.最少交换次数来组合所有的1](https://zhuanlan.zhihu.com/p/610881708) · 知乎 · 2023-03-02 · 赞同 1**
> 力扣：[1151. 最少交换次数来组合所有的1](https://leetcode.cn/problems/minimum-swaps-to-group-all-1s-together/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1151.最少交换次数来组合所有的1

[力扣](https://leetcode.cn/problems/minimum-swaps-to-group-all-1s-together/)

交换完成后数组中必然会得到一段长度为k的连续的1，而交换的代价就是k减去这一段中原本就是1的位置的数量。为了使得交换的代价最小，实际上就是要找到数组中长度为k的区间，且这个区间中的1最多。

这个问题是最标准的滑动窗口问题，按照常规滑动窗口的做法处理即可。

最后附上python代码：

```python
class Solution(object):
    def minSwaps(self, data):
        """
        :type data: List[int]
        :rtype: int
        """

        k = sum(data)
        now = sum(data[:k])
        res = k - now
        for index, num in enumerate(data[k:]):
            now += num - data[index]
            res = min(res, k - now)
        
        return res
```
