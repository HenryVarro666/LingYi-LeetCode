---
title: "875. 爱吃香蕉的珂珂"
aliases: ["yiduobo的每日leetcode 875.爱吃香蕉的珂珂"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350564052"
zhihu_id: "350564052"
zhihu_title: "yiduobo的每日leetcode 875.爱吃香蕉的珂珂"
question_id: "875"
question: "爱吃香蕉的珂珂"
problem_url: "https://leetcode.cn/problems/koko-eating-bananas/"
difficulty: "Medium"
rating: 1766
created: "2021-02-15T02:49:03+08:00"
updated: "2021-02-15T02:49:03+08:00"
upvotes: 0
comments: 0
---

# 875. 爱吃香蕉的珂珂

> **[yiduobo的每日leetcode 875.爱吃香蕉的珂珂](https://zhuanlan.zhihu.com/p/350564052) · 知乎 · 2021-02-15 · 赞同 0**
> 力扣：[875. 爱吃香蕉的珂珂](https://leetcode.cn/problems/koko-eating-bananas/) · Medium · 灵茶山艾府：[二分答案（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

875.爱吃香蕉的珂珂

[力扣](https://leetcode-cn.com/problems/koko-eating-bananas/)

虽然K的增大，吃完所有香蕉所需的时间必然是单调递减的，因此在这里可以二分K，然后判断以K的速度能否在H小时内吃完所有香蕉。

对于二分的边界，下界自然是1，而上界则是max(piles)，因此更大的K相比max(piles)是没有意义的。

最后附上python代码：

```python
class Solution(object):
    def minEatingSpeed(self, piles, H):
        """
        :type piles: List[int]
        :type H: int
        :rtype: int
        """

        l = 1
        r = max(piles)
        while l < r:
            cnt = 0
            mid = (l + r) >> 1
            for pile in piles:
                cnt += pile / mid
                if pile % mid != 0:
                    cnt += 1
            if cnt > H:
                l = mid + 1
            else:
                r = mid
        
        return l
```
