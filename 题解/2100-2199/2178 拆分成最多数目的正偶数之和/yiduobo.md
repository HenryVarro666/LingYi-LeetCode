---
title: "2178. 拆分成最多数目的正偶数之和"
aliases: ["yiduobo的每日leetcode 2178.拆分成最多数目的正偶数之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/535135342"
zhihu_id: "535135342"
zhihu_title: "yiduobo的每日leetcode 2178.拆分成最多数目的正偶数之和"
question_id: "2178"
question: "拆分成最多数目的正偶数之和"
problem_url: "https://leetcode.cn/problems/maximum-split-of-positive-even-integers/"
difficulty: "Medium"
rating: 1538
created: "2022-06-29T00:22:15+08:00"
updated: "2022-06-29T00:22:15+08:00"
upvotes: 0
comments: 0
---

# 2178. 拆分成最多数目的正偶数之和

> **[yiduobo的每日leetcode 2178.拆分成最多数目的正偶数之和](https://zhuanlan.zhihu.com/p/535135342) · 知乎 · 2022-06-29 · 赞同 0**
> 力扣：[2178. 拆分成最多数目的正偶数之和](https://leetcode.cn/problems/maximum-split-of-positive-even-integers/) · Medium · 灵茶山艾府：[贪心 + 简洁写法（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2178.拆分成最多数目的正偶数之和

[力扣](https://leetcode.cn/problems/maximum-split-of-positive-even-integers/)

首先，若干个偶数之和还是偶数，因此若finalSum不是偶数，那么就无法进行拆分，此时直接返回空。

接下来考虑finalSum为偶数的情况。由于拆分出来的偶数不能重复，为了使得拆分的数量尽可能多，那么就应该从小的偶数开始拆分，也就是从2、4、6开始往上拆分。

由于不能重复，那么按2、4、6这样递增地拆分了k个偶数之后，剩下的最后一个偶数必然要大于2k，也就是

finalSum - (2 + 4 + ... + 2k) > 2k

整理一下就是

finalSum > (3 + k) \* k

那么只需找出最大的满足条件的k，最终答案就是2、4、...、2k再加上finalSum - k \* (k + 1)

最后附上python代码：

```python
class Solution(object):
    def maximumEvenSplit(self, finalSum):
        """
        :type finalSum: int
        :rtype: List[int]
        """

        if finalSum % 2 == 1:
            return []
        
        k = int(sqrt(finalSum))
        while k > 0 and k * (k + 3) >= finalSum:
            k -= 1
        
        res = []
        for index in range(k):
            res.append(index * 2 + 2)
        res.append(finalSum - k * (k + 1))
        return res
```
