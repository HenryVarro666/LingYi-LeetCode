---
title: "2106. 摘水果"
aliases: ["yiduobo的每日leetcode 2106.摘水果"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/binary-search", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/522807269"
zhihu_id: "522807269"
zhihu_title: "yiduobo的每日leetcode 2106.摘水果"
question_id: "2106"
question: "摘水果"
problem_url: "https://leetcode.cn/problems/maximum-fruits-harvested-after-at-most-k-steps/"
difficulty: "Hard"
rating: 2062
created: "2022-06-01T00:20:27+08:00"
updated: "2022-06-01T00:20:27+08:00"
upvotes: 0
comments: 0
---

# 2106. 摘水果

> **[yiduobo的每日leetcode 2106.摘水果](https://zhuanlan.zhihu.com/p/522807269) · 知乎 · 2022-06-01 · 赞同 0**
> 力扣：[2106. 摘水果](https://leetcode.cn/problems/maximum-fruits-harvested-after-at-most-k-steps/) · Hard · 灵茶山艾府：[滑动窗口，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2106.摘水果

[力扣](https://leetcode.cn/problems/maximum-fruits-harvested-after-at-most-k-steps/)

由于摘掉的水果就没了，因此最终只可能有两种走法，即：

1、先向左走到某个位置left，然后再从left开始尽力向右走。

在这种情况下，由于先向左走了startPos - left步，那么从left开始向右还可以走k - (startPos - left)步，最终可以到达的位置就是min(n, left + k - (startPos - left))。

当然，这个位置可能依然在startPos的左边，因此最终走过的区间就是

[left, max(startPos, min(n, left + k - (startPos - left)))]

之后的问题就是计算区间内水果的数目并更新答案。这是一个典型的区间和问题，可以利用前缀和来进行优化，从而在O(1)的时间内得到区间内水果的数目。

2、先向右走到某个位置right，然后再从right开始尽力向左走

与上面类似，由于先向右走了right - startPos步，那么从right开始向左还可以走k - (right - startPos)步，最终可以到达的位置就是max(0, right - (k - (right - startPos)))。

同样的额，这个位置可能依然在startPos的右边，因此最终走过的区间就是

[min(startPos, max(0, right - (k - (right - startPos)))), right]

同样地，利用前缀和计算区间内水果的数目并更新答案即可。

由于数轴的长度不超过200000，那么完全可以枚举每个left和right的位置，然后利用上面的做法计算这种走法能拿到的水果数目，取其中拿到水果最多的作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxTotalFruits(self, fruits, startPos, k):
        """
        :type fruits: List[List[int]]
        :type startPos: int
        :type k: int
        :rtype: int
        """

        n = max(fruits[-1][0], startPos)
        s = [0] * (n + 1)
        for pos, amount in fruits:
            s[pos] = amount
        
        for index in range(1, n + 1):
            s[index] += s[index - 1]
        
        res = 0
        for left in range(max(0, startPos - k), startPos + 1):
            right = max(startPos, min(left + k - (startPos - left), n))
            cnt = s[right]
            if left > 0:
                cnt -= s[left - 1]
            
            res = max(res, cnt)
        
        for right in range(startPos + 1, min(n, startPos + k) + 1):
            left = min(startPos, max(right - (k - (right - startPos)), 0))
            cnt = s[right]
            if left > 0:
                cnt -= s[left - 1]
            
            res = max(res, cnt)
        
        return res
```
