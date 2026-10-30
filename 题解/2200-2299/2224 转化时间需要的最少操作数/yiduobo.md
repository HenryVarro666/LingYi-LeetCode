---
title: "2224. 转化时间需要的最少操作数"
aliases: ["yiduobo的每日leetcode 2224.转化时间需要的最少操作数"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/542705864"
zhihu_id: "542705864"
zhihu_title: "yiduobo的每日leetcode 2224.转化时间需要的最少操作数"
question_id: "2224"
question: "转化时间需要的最少操作数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-convert-time/"
difficulty: "Easy"
created: "2022-07-17T18:33:08+08:00"
updated: "2022-07-17T18:33:08+08:00"
upvotes: 0
comments: 0
---

# 2224. 转化时间需要的最少操作数

> **[yiduobo的每日leetcode 2224.转化时间需要的最少操作数](https://zhuanlan.zhihu.com/p/542705864) · 知乎 · 2022-07-17 · 赞同 0**
> 力扣：[2224. 转化时间需要的最少操作数](https://leetcode.cn/problems/minimum-number-of-operations-to-convert-time/) · Easy · 灵茶山艾府：[从大往小贪心 + 简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2224.转化时间的需要的最少操作数

[力扣](https://leetcode.cn/problems/minimum-number-of-operations-to-convert-time/)

乍一看似乎是背包问题，但是实际上由于60、15、5、1之间具有倍数关系，因此在这里可以使用贪心。具体来说就是先将两个时间转化成分钟表示，计算二者的差值，然后对于这个差值先尽量用60去填充，无法填充的部分再依次尽量用15、5和1去填充。

最后附上python代码：

```python
class Solution(object):
    def convertTime(self, current, correct):
        """
        :type current: str
        :type correct: str
        :rtype: int
        """

        m1 = int(current[:2]) * 60 + int(current[3:])
        m2 = int(correct[:2]) * 60 + int(correct[3:])
        
        now = m2 - m1
        res = 0
        delta_list = [60, 15, 5, 1]
        for delta in delta_list:
            res += now / delta
            now %= delta
        
        return res
```
