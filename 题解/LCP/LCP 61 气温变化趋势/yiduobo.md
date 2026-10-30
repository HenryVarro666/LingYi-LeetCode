---
title: "LCP 61. 气温变化趋势"
aliases: ["yiduobo的每日leetcode LCP61.气温变化趋势"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/api"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/579203362"
zhihu_id: "579203362"
zhihu_title: "yiduobo的每日leetcode LCP61.气温变化趋势"
question_id: "LCP 61"
question: "气温变化趋势"
problem_url: "https://leetcode.cn/problems/6CE719/"
difficulty: "Easy"
created: "2022-11-01T00:51:50+08:00"
updated: "2022-11-01T00:51:50+08:00"
upvotes: 0
comments: 0
---

# LCP 61. 气温变化趋势

> **[yiduobo的每日leetcode LCP61.气温变化趋势](https://zhuanlan.zhihu.com/p/579203362) · 知乎 · 2022-11-01 · 赞同 0**
> 力扣：[LCP 61. 气温变化趋势](https://leetcode.cn/problems/6CE719/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP61.气温变化趋势

[力扣](https://leetcode.cn/problems/6CE719/)

使用一个变量cnt记录变化趋势相同的最长连续天数，然后从下标位置1开始向后开始遍历，根据当前气温和前一天气温来计算两地当天的气温变化趋势。若趋势相同，则将cnt加上1，否则使用cnt来更新答案，然后将cnt重置为0。另外，在遍历完成后，需要使用当前的cnt再更新一次答案。

最后附上python代码：

```python
class Solution(object):
    def temperatureTrend(self, temperatureA, temperatureB):
        """
        :type temperatureA: List[int]
        :type temperatureB: List[int]
        :rtype: int
        """

        n = len(temperatureA)
        res = 0
        cnt = 0
        for index in range(1, n):
            if temperatureA[index] > temperatureA[index - 1]:
                flagA = 1
            elif temperatureA[index] == temperatureA[index - 1]:
                flagA = 0
            else:
                flagA = -1
            
            if temperatureB[index] > temperatureB[index - 1]:
                flagB = 1
            elif temperatureB[index] == temperatureB[index - 1]:
                flagB = 0
            else:
                flagB = -1
            
            if flagA == flagB:
                cnt += 1
            else:
                res = max(res, cnt)
                cnt = 0
        
        return max(res, cnt)
```
