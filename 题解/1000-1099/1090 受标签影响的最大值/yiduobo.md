---
title: "1090. 受标签影响的最大值"
aliases: ["yiduobo的每日leetcode 1090.受标签影响的最大值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/373383732"
zhihu_id: "373383732"
zhihu_title: "yiduobo的每日leetcode 1090.受标签影响的最大值"
question_id: "1090"
question: "受标签影响的最大值"
problem_url: "https://leetcode.cn/problems/largest-values-from-labels/"
created: "2021-05-18T22:14:49+08:00"
updated: "2021-05-18T22:14:49+08:00"
upvotes: 0
comments: 0
---

# 1090. 受标签影响的最大值

> **[yiduobo的每日leetcode 1090.受标签影响的最大值](https://zhuanlan.zhihu.com/p/373383732) · 知乎 · 2021-05-18 · 赞同 0**
> 力扣：[1090. 受标签影响的最大值](https://leetcode.cn/problems/largest-values-from-labels/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1090.受标签影响的最大值

[力扣](https://leetcode-cn.com/problems/largest-values-from-labels/)

贪心法的题目。对于同样label的两项，显然应当优先选择较大的那一项。对于label不同的两项，在没有limit限制且只能选择其中一项时，也应当优先选择较大的那一项。于是可以按照values从大到小进行排序，接下来一趟扫描，若当前项对应的label还未达到limit，就将对应的value加入到答案中，直到选出wanted个数或者扫描结束。

最后附上python代码：

```python
class Solution(object):
    def largestValsFromLabels(self, values, labels, num_wanted, use_limit):
        """
        :type values: List[int]
        :type labels: List[int]
        :type num_wanted: int
        :type use_limit: int
        :rtype: int
        """

        used = {}
        n = len(values)
        res = 0
        for value, label in sorted([[values[index], labels[index]] for index in range(n)], key=lambda d:d[0], reverse=True):
            if used.get(label, 0) < use_limit:
                used[label] = used.get(label, 0) + 1
                res += value
                num_wanted -= 1
                if num_wanted == 0:
                    break

        return res
```
