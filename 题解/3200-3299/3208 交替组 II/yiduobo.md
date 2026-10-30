---
title: "3208. 交替组II"
aliases: ["yiduobo的每日leetcode 3208.交替组II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707954227"
zhihu_id: "707954227"
zhihu_title: "yiduobo的每日leetcode 3208.交替组II"
question_id: "3208"
question: "交替组 II"
problem_url: "https://leetcode.cn/problems/alternating-groups-ii/"
difficulty: "Medium"
created: "2024-07-09T23:51:46+08:00"
updated: "2024-07-09T23:51:46+08:00"
upvotes: 0
comments: 0
---

# 3208. 交替组II

> **[yiduobo的每日leetcode 3208.交替组II](https://zhuanlan.zhihu.com/p/707954227) · 知乎 · 2024-07-09 · 赞同 0**
> 力扣：[3208. 交替组 II](https://leetcode.cn/problems/alternating-groups-ii/) · Medium · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3208.交替组II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/alternating-groups-ii/description/)

题目给出一个长度为n，由01组成的数组colors，表示环形瓷砖的颜色。其中colors[i]等于0时表示第i块瓷砖的颜色为红色，等于1时则表示第i块瓷砖的颜色为蓝色。另外给出一个整数k，如果数组中连续k块瓷砖的颜色是交替颜色，也就是说除了第一块和最后一块瓷砖之外，其他瓷砖的颜色都和其左侧和右侧瓷砖的颜色的不同，那么这就是一个交替组。问一共有多少个交替组。

之前3206题的加强版，本题中的交替组要求长度为k。方便起见，现将colors原样复制一份，这样一来就就环形问题转化成了线性问题。

使用一个变量start表示当前交替组的起点，接下来：

1、对于当前的start，使用一个变量p从start + 1开始向后检测，若当前的colors[p]不等于colors[p - 1]，就将p向后移动，直到p - start \= k为止，此时的colors[start : p]就是一个交替组；反之，若过程中出现了colors[p]等于colors[p - 1]的情况，那么就不可能存在以start到p - 1中任意位置为起点的交替组，此时应该将start更新为p。重复此过程直到找出一个交替组或者start等于n为止。

2、若找到了交替组colors[start : p]，就可以继续向后检测。若当前的start + 1小于n，同时colors[p]不等于colors[p - 1]，此时就说明colors[start + 1 : p + 1]也是一个交替组，此时就应该将start和p都向后移动，同时更新答案。重复此过程直到start等于n或者colors[p]等于colors[p - 1]。若此时的start依然小于n，那么就将其更新为p，然后回到步骤1继续寻找下一段交替组。

最后附上python代码：

```python
class Solution(object):
    def numberOfAlternatingGroups(self, colors, k):
        """
        :type colors: List[int]
        :type k: int
        :rtype: int
        """

        n = len(colors)
        colors += colors
        start = 0
        p = 1
        res = 0
        while start < n:
            while p - start < k and colors[p] != colors[p - 1]:
                p += 1

            if p - start == k:
                res += 1
                while start + 1 < n and colors[p] != colors[p - 1]:
                    p += 1
                    start += 1
                    res += 1
                
            if start < n:
                start = p
                p += 1
        
        return res
```
