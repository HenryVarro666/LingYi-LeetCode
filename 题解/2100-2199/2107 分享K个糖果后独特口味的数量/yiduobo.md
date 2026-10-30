---
title: "2107. 分享K个糖果后独特口味的数量"
aliases: ["yiduobo的每日leetcode 2107.分享K个糖果后独特口味的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/626225821"
zhihu_id: "626225821"
zhihu_title: "yiduobo的每日leetcode 2107.分享K个糖果后独特口味的数量"
question_id: "2107"
question: "分享K个糖果后独特口味的数量"
problem_url: "https://leetcode.cn/problems/number-of-unique-flavors-after-sharing-k-candies/"
created: "2023-05-02T04:59:38+08:00"
updated: "2023-05-02T04:59:38+08:00"
upvotes: 0
comments: 0
---

# 2107. 分享K个糖果后独特口味的数量

> **[yiduobo的每日leetcode 2107.分享K个糖果后独特口味的数量](https://zhuanlan.zhihu.com/p/626225821) · 知乎 · 2023-05-02 · 赞同 0**
> 力扣：[2107. 分享K个糖果后独特口味的数量](https://leetcode.cn/problems/number-of-unique-flavors-after-sharing-k-candies/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2107.分享K个糖果后独特口味的数量

[力扣](https://leetcode.cn/problems/number-of-unique-flavors-after-sharing-k-candies/)

本题要求从数组中移除一个子数组，使得数组中剩余数字的种类最多，属于是滑动窗口问题的反向版。与常规的滑动窗口问题不同，本题需要维护的是窗口滑动过程中在窗口外的每种数字的个数。

具体实现上，同样是使用一个长度为K的窗口从头开始向后滑动，同时使用一个哈希表cnt记录每种数字出现的次数。

当窗口向后滑动时，将当前被移出窗口的数字在哈希表中的次数加上1，同时将新加入窗口的数字从哈希表中的次数减去1，然后使用哈希表的长度来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def shareCandies(self, candies, k):
        """
        :type candies: List[int]
        :type k: int
        :rtype: int
        """

        cnt = {}
        for v in candies[k:]:
            cnt[v] = cnt.get(v, 0) + 1
        
        res = len(cnt)
        for index, v in enumerate(candies[k:]):
            cnt[candies[index]] = cnt.get(candies[index], 0) + 1
            cnt[v] -= 1
            if cnt[v] == 0:
                cnt.pop(v)
            
            res = max(res, len(cnt))
        
        return res
```
