---
title: "1891. 割绳子"
aliases: ["yiduobo的每日leetcode 1891.割绳子"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/622996592"
zhihu_id: "622996592"
zhihu_title: "yiduobo的每日leetcode 1891.割绳子"
question_id: "1891"
question: "割绳子"
problem_url: "https://leetcode.cn/problems/cutting-ribbons/"
created: "2023-04-19T00:29:49+08:00"
updated: "2023-04-19T00:29:49+08:00"
upvotes: 0
comments: 0
---

# 1891. 割绳子

> **[yiduobo的每日leetcode 1891.割绳子](https://zhuanlan.zhihu.com/p/622996592) · 知乎 · 2023-04-19 · 赞同 0**
> 力扣：[1891. 割绳子](https://leetcode.cn/problems/cutting-ribbons/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1891.割绳子

[力扣](https://leetcode.cn/problems/cutting-ribbons/)

又是这个经典的题型，与之前2226题完全相同，直接套用之前2226题相同的处理方法就行了。

[yiduobo：yiduobo的每日leetcode 2226.每个小孩最多能分到多少糖果](https://zhuanlan.zhihu.com/p/543264736)

最后附上python代码：

```python
class Solution(object):
    def maxLength(self, ribbons, k):
        """
        :type ribbons: List[int]
        :type k: int
        :rtype: int
        """

        left = 0
        right = max(ribbons)
        while left < right:
            mid = (left + right + 1) / 2
            cnt = 0
            for r in ribbons:
                cnt += r / mid
            
            if cnt >= k:
                left = mid
            else:
                right = mid - 1
        
        return left
```
