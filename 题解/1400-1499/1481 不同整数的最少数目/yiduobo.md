---
title: "1481. 不同整数的最少数目"
aliases: ["yiduobo的每日leetcode 1481.不同整数的最少数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/415903870"
zhihu_id: "415903870"
zhihu_title: "yiduobo的每日leetcode 1481.不同整数的最少数目"
question_id: "1481"
question: "不同整数的最少数目"
problem_url: "https://leetcode.cn/problems/least-number-of-unique-integers-after-k-removals/"
created: "2021-09-30T21:42:25+08:00"
updated: "2021-09-30T21:42:25+08:00"
upvotes: 0
comments: 0
---

# 1481. 不同整数的最少数目

> **[yiduobo的每日leetcode 1481.不同整数的最少数目](https://zhuanlan.zhihu.com/p/415903870) · 知乎 · 2021-09-30 · 赞同 0**
> 力扣：[1481. 不同整数的最少数目](https://leetcode.cn/problems/least-number-of-unique-integers-after-k-removals/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1481.不同整数的最少数目

[力扣](https://leetcode-cn.com/problems/least-number-of-unique-integers-after-k-removals/)

为了使得剩下的不同整数数目最少，显然应该优先移除出现次数较少的那些整数，于是可以先一趟扫描，统计每种整数出现的数目。接下来按次数从小到大进行排序，然后再一趟遍历尽可能多地移除整数。

最后附上python代码：

```python
class Solution(object):
    def findLeastNumOfUniqueInts(self, arr, k):
        """
        :type arr: List[int]
        :type k: int
        :rtype: int
        """

        cnt_dict = {}
        for num in arr:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        res = len(cnt_dict)
        for cnt in sorted(cnt_dict.values()):
            if cnt <= k:
                res -= 1
                k -= cnt
        
        return res
```
