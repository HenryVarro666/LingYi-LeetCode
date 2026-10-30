---
title: "248. 中心对称数III"
aliases: ["yiduobo的每日leetcode 248.中心对称数III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/592176151"
zhihu_id: "592176151"
zhihu_title: "yiduobo的每日leetcode 248.中心对称数III"
question_id: "248"
question: "中心对称数III"
problem_url: "https://leetcode.cn/problems/strobogrammatic-number-iii/"
created: "2022-12-16T04:59:32+08:00"
updated: "2022-12-16T04:59:32+08:00"
upvotes: 0
comments: 2
---

# 248. 中心对称数III

> **[yiduobo的每日leetcode 248.中心对称数III](https://zhuanlan.zhihu.com/p/592176151) · 知乎 · 2022-12-16 · 赞同 0**
> 力扣：[248. 中心对称数III](https://leetcode.cn/problems/strobogrammatic-number-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

248.中心对称数III

[力扣](https://leetcode.cn/problems/strobogrammatic-number-iii/)

看上去最好的做法应该是基于数位的动态规划，或者提前预处理出每种长度的中心对称数的数量，然后分情况讨论也可以。不过注意到之前247题，最终长度为14的中心对称数也才62500个，那么完全可以根据high的长度n计算出所有长度小于等于n的中心对称数，然后一趟遍历，统计大小处于low到high之间的数就行了。

最后附上python代码：

```python
class Solution(object):
    def strobogrammaticInRange(self, low, high):
        """
        :type low: str
        :type high: str
        :rtype: int
        """

        f = []
        f.append([''])
        f.append(['0', '1', '8'])

        n = len(high)

        for index in range(2, n + 1):
            f.append([])
            for s in f[index - 2]:
                f[-1].append('0' + s + '0')
                f[-1].append('1' + s + '1')
                f[-1].append('6' + s + '9')
                f[-1].append('8' + s + '8')
                f[-1].append('9' + s + '6')
    
        res = 0
        low, high = int(low), int(high)
        for index in range(1, n + 1):
            for s in f[index]:
                if index == 1 or s[0] != '0':
                    if low <= int(s) <= high:
                        res += 1     

        return res
```
