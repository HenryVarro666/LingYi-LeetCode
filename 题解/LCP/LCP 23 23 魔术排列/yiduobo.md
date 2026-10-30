---
title: "LCP 23. 魔术排列"
aliases: ["yiduobo的每日leetcode LCP23.魔术排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/573051918"
zhihu_id: "573051918"
zhihu_title: "yiduobo的每日leetcode LCP23.魔术排列"
question_id: "LCP 23"
question: "魔术排列"
problem_url: "https://leetcode.cn/problems/er94lq/"
created: "2022-10-13T01:32:00+08:00"
updated: "2022-10-13T01:32:00+08:00"
upvotes: 0
comments: 0
---

# LCP 23. 魔术排列

> **[yiduobo的每日leetcode LCP23.魔术排列](https://zhuanlan.zhihu.com/p/573051918) · 知乎 · 2022-10-13 · 赞同 0**
> 力扣：[LCP 23. 魔术排列](https://leetcode.cn/problems/er94lq/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP23.魔术排列

[力扣](https://leetcode.cn/problems/er94lq/)

对于题目中给出的重排列方式，在每次取走前k张牌之后，第k + 1张牌在下一轮必然会被洗到牌堆的后半部分去，那么如果在首轮洗牌后牌堆与target前缀匹配的长度p大于k，那么在第二轮洗牌后target[k]必然是无法成功匹配的，想要匹配的话必须将k调整到刚好等于p。也就是说，题目中唯一合法的k在第一轮洗牌之后就已经确定下来了。

得到k之后，只需不断模拟洗牌过程，然后判断是否与target匹配就行了。最坏情况下，一共需要执行n次洗牌，总的时间复杂度就是O(n^2)。

最后附上python代码：

```python
class Solution(object):
    def isMagic(self, target):
        """
        :type target: List[int]
        :rtype: bool
        """

        n = len(target)
        first = []
        for index in range(1, n + 1):
            if index % 2 == 0:
                first.append(index)
        for index in range(1, n + 1):
            if index % 2 == 1:
                first.append(index)
        
        k = 0
        while k < n and first[k] == target[k]:
            k += 1
        
        if k == n:
            return True
        
        if k == 0:
            return False
        
        p = k
        now = first[k:]
        while True:
            next = []
            for index in range(len(now)):
                if index % 2 == 1:
                    next.append(now[index])
            for index in range(len(now)):
                if index % 2 == 0:
                    next.append(now[index])

            if len(next) > k:
                for index in range(k):
                    if target[p + index] != next[index]:
                        return False
                now = next[k:]
                p += k
            else:
                for index in range(len(next)):
                    if target[p + index] != next[index]:
                        return False
                break
        
        return True
```
