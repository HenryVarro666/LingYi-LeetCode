---
title: "3945. 计算数字频率得分"
aliases: ["yiduobo的每日leetcode 3945.计算数字频率得分"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2044521371728883963"
zhihu_id: "2044521371728883963"
zhihu_title: "yiduobo的每日leetcode 3945.计算数字频率得分"
question_id: "3945"
question: "计算数字频率得分"
problem_url: "https://leetcode.cn/problems/digit-frequency-score/"
difficulty: "Easy"
created: "2026-05-31T20:54:14+08:00"
updated: "2026-05-31T20:54:14+08:00"
upvotes: 0
comments: 0
---

# 3945. 计算数字频率得分

> **[yiduobo的每日leetcode 3945.计算数字频率得分](https://zhuanlan.zhihu.com/p/2044521371728883963) · 知乎 · 2026-05-31 · 赞同 0**
> 力扣：[3945. 计算数字频率得分](https://leetcode.cn/problems/digit-frequency-score/) · Easy · 灵茶山艾府：[数位和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3945.计算数字频率得分

<https://leetcode.cn/problems/digit-frequency-score/>

题目给出一个整数n。

n的得分定义为，对于n中所有的不同数字d，计算d \* freq(d)的总和，其中freq(d)表示d在n中出现的次数。

问n的得分是多少。

按照题目描述直接模拟计算即可。

使用模10除以10的方法分离n的所有数位d，并使用哈希表freq记录其中每种d出现的次数。接下来遍历freq中的每种d，将d \* freq[d]累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def digitFrequencyScore(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        freq = {}
        while n:
            d = n % 10
            n //= 10
            freq[d] = freq.get(d, 0) + 1
        
        res = 0
        for d in freq:
            res += d * freq[d]
        
        return res
```
