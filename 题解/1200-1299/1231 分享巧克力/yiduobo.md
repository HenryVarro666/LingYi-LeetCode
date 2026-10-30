---
title: "1231. 分享巧克力"
aliases: ["yiduobo的每日leetcode 1231.分享巧克力"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/614037716"
zhihu_id: "614037716"
zhihu_title: "yiduobo的每日leetcode 1231.分享巧克力"
question_id: "1231"
question: "分享巧克力"
problem_url: "https://leetcode.cn/problems/divide-chocolate/"
created: "2023-03-14T23:12:45+08:00"
updated: "2023-03-14T23:12:46+08:00"
upvotes: 0
comments: 0
---

# 1231. 分享巧克力

> **[yiduobo的每日leetcode 1231.分享巧克力](https://zhuanlan.zhihu.com/p/614037716) · 知乎 · 2023-03-14 · 赞同 0**
> 力扣：[1231. 分享巧克力](https://leetcode.cn/problems/divide-chocolate/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1231.分享巧克力

[力扣](https://leetcode.cn/problems/divide-chocolate/)

之前410题的翻版

[yiduobo：yiduobo的每日leetcode 410.分割数组的最大值](https://zhuanlan.zhihu.com/p/187591149)

不过之前410题要求的是分割数组的最大值最小，而本题则是最小值最大，在这里只需要注意符号要反过来。相对应的，二分上下界的变化以及二分中点的计算方式也要做出相应的调整。

最后附上python代码：

```python
class Solution(object):
    def maximizeSweetness(self, sweetness, k):
        """
        :type sweetness: List[int]
        :type k: int
        :rtype: int
        """

        left = min(sweetness)
        right = sum(sweetness)

        while left < right:
            mid = (left + right + 1) / 2

            cnt = 0
            s = 0
            for v in sweetness:
                s += v
                if s >= mid:
                    cnt += 1
                    s = 0

            if cnt >= k + 1:
                left = mid
            else:
                right = mid - 1
        
        return left
```
