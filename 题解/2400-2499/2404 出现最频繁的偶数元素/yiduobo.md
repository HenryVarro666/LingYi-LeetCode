---
title: "2404. 出现最频繁的偶数元素"
aliases: ["yiduobo的每日leetcode 2404.出现最频繁的偶数元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/567649148"
zhihu_id: "567649148"
zhihu_title: "yiduobo的每日leetcode 2404.出现最频繁的偶数元素"
question_id: "2404"
question: "出现最频繁的偶数元素"
problem_url: "https://leetcode.cn/problems/most-frequent-even-element/"
difficulty: "Easy"
created: "2022-09-24T04:34:07+08:00"
updated: "2022-09-24T04:34:07+08:00"
upvotes: 1
comments: 0
---

# 2404. 出现最频繁的偶数元素

> **[yiduobo的每日leetcode 2404.出现最频繁的偶数元素](https://zhuanlan.zhihu.com/p/567649148) · 知乎 · 2022-09-24 · 赞同 1**
> 力扣：[2404. 出现最频繁的偶数元素](https://leetcode.cn/problems/most-frequent-even-element/) · Easy · 灵茶山艾府：[一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2404.出现最频繁的偶数元素

[力扣](https://leetcode.cn/problems/most-frequent-even-element/)

一趟遍历，使用哈希表记录每种偶数出现的次数，选其中出现次数最多的作为答案即可。需要注意的是，当两种偶数出现次数相同时，需要选择较小的偶数作为答案。

最后附上python代码：

```python
class Solution(object):
    def mostFrequentEven(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        cnt = {}
        res = -1
        cnt[-1] = 0

        for num in nums:
            if num % 2 == 0:
                cnt[num] = cnt.get(num, 0) + 1
            
                if cnt[num] > cnt[res] or (cnt[num] == cnt[res] and num < res):
                    res = num
        
        return res
```
