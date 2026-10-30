---
title: "1711. 大餐计数"
aliases: ["yiduobo的每日leetcode 1711.大餐计数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/449882582"
zhihu_id: "449882582"
zhihu_title: "yiduobo的每日leetcode 1711.大餐计数"
question_id: "1711"
question: "大餐计数"
problem_url: "https://leetcode.cn/problems/count-good-meals/"
created: "2021-12-25T23:01:21+08:00"
updated: "2021-12-25T23:01:21+08:00"
upvotes: 0
comments: 0
---

# 1711. 大餐计数

> **[yiduobo的每日leetcode 1711.大餐计数](https://zhuanlan.zhihu.com/p/449882582) · 知乎 · 2021-12-25 · 赞同 0**
> 力扣：[1711. 大餐计数](https://leetcode.cn/problems/count-good-meals/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1711.大餐计数

[力扣](https://leetcode-cn.com/problems/count-good-meals/)

首先确定美味程度之和的范围。不妨设数组中的最大值为max，p为满足2^p > max的最小的p，那么必然就有max + x \< 2^(p + 1)，也就是说最后只需要考察2^0到2^p这些美味程度之和了。由于这里的max \<\= 2^20，因此这里的p最大为21，那么实际上需要考察的美味程度之和是很少的。

具体实现上，自然是使用哈希表储存每个数字出现的次数。接下来遍历每个数字num，并枚举美味程度之和2^p。设num出现的次数为cnt1，2^p - num出现的次数为cnt2，那么此时应该使用cnt1 \* cnt2来更新答案。当然，这个计算方法可能会出现重复计算的情况，为了不重复计算，在这里可以假设num \* 2 \< p，这样就不会重复计算了。除此之外，还有一种特殊情况是num \* 2 \= p，此时相当于从cnt个num中选择两个，对应的就是cnt \* (cnt - 1) / 2。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, deliciousness):
        """
        :type deliciousness: List[int]
        :rtype: int
        """

        pow2 = [1]
        num_dict = {}
        for v in deliciousness:
            num_dict[v] = num_dict.get(v, 0) + 1
            while pow2[-1] <= v:
                pow2.append(pow2[-1] + pow2[-1])
        
        mod = 10 ** 9 + 7
        res = 0

        for v, cnt in num_dict.items():
            for p in pow2:
                if v + v == p:
                    res += cnt * (cnt - 1) / 2 % mod
                elif v + v < p:
                    res += cnt * num_dict.get(p - v, 0) % mod
                    
        return res
```
