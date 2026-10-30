---
title: "1375. 灯泡开关III"
aliases: ["yiduobo的每日leetcode 1375.灯泡开关III"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/401595014"
zhihu_id: "401595014"
zhihu_title: "yiduobo的每日leetcode 1375.灯泡开关III"
question_id: "1375"
question: "二进制字符串前缀一致的次数"
problem_url: "https://leetcode.cn/problems/number-of-times-binary-string-is-prefix-aligned/"
difficulty: "Medium"
created: "2021-08-19T22:20:12+08:00"
updated: "2021-08-19T22:20:12+08:00"
upvotes: 0
comments: 0
---

# 1375. 灯泡开关III

> **[yiduobo的每日leetcode 1375.灯泡开关III](https://zhuanlan.zhihu.com/p/401595014) · 知乎 · 2021-08-19 · 赞同 0**
> 力扣：[1375. 二进制字符串前缀一致的次数](https://leetcode.cn/problems/number-of-times-binary-string-is-prefix-aligned/) · Medium · 灵茶山艾府：[巧妙利用性质，维护最大值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1375.灯泡开关III

[力扣](https://leetcode-cn.com/problems/bulb-switcher-iii/)

首先，由于light是1到n的一个排列，那么其中数字必然各不相同，因此已经打开的灯是不会关上的。

接下来，对于某一时刻k，必然已经打开了k盏灯。为了使得这些灯都是蓝色，那么必须要打开1到k这些灯才行。于是一个可行的做法是遍历light，对于每一时刻k，若此时的light[:k]恰好是1到k的一个排列，那么说明k是一个符合题目要求的时刻。

当然，直接判断是否为1到k的一个排列复杂度较高，一个可行的做法是计算sum(light[:k])，若这个值恰好等于(1 + k) \* k / 2，那么说明这就是k的一个排列。计算sum的过程则可以转化为前缀和均摊到每一轮来处理。

最后附上python代码：

```python
class Solution(object):
    def numTimesAllBlue(self, light):
        """
        :type light: List[int]
        :rtype: int
        """

        s = 0
        now = 0
        res = 0
        for index, num in enumerate(light):
            s += index + 1
            now += num
            if s == now:
                res += 1
        
        return res
```
