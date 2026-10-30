---
title: "3361. 两个字符串的切换距离"
aliases: ["yiduobo的每日leetcode 3361.两个字符串的切换距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/27335543680"
zhihu_id: "27335543680"
zhihu_title: "yiduobo的每日leetcode 3361.两个字符串的切换距离"
question_id: "3361"
question: "两个字符串的切换距离"
problem_url: "https://leetcode.cn/problems/shift-distance-between-two-strings/"
difficulty: "Medium"
created: "2025-03-01T23:51:02+08:00"
updated: "2025-03-01T23:51:44+08:00"
upvotes: 0
comments: 0
---

# 3361. 两个字符串的切换距离

> **[yiduobo的每日leetcode 3361.两个字符串的切换距离](https://zhuanlan.zhihu.com/p/27335543680) · 知乎 · 2025-03-01 · 赞同 0**
> 力扣：[3361. 两个字符串的切换距离](https://leetcode.cn/problems/shift-distance-between-two-strings/) · Medium · 灵茶山艾府：[前缀和 O(n) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3361.两个字符串的切换距离

[3361. 两个字符串的切换距离 - 力扣（LeetCode）](https://leetcode.cn/problems/shift-distance-between-two-strings/description/)

题目给出两个长度相等的字符串s和t，以及两个整数数组nextCost和previousCost。接下来每次操作中，可以任意选择s中的一个下标i，将其变为字母表中的下一个字符或者上一个字符。若切换为下一个字符，切换的代价为nextCost[j]，其中j为s[i]在字母表中的下标，若切换为上一个字符，切换的代价为previousCost[j]，其中j同样是s[i]在字母表中的下标。

问将s变为t所需的最少操作代价。

题目要求计算将s变为t所需的最小代价，而每次操作针对单个字符是互相独立的，换言之只需一趟遍历，计算将每个s[i]变为t[i]所需的最小代价，然后累加即为最终答案。

接下来考察单次操作中的代价应该如何计算。对于s[i]和t[i]：

1、若s[i]和t[i]相同：

这种情况下无需变换，代价为0

2、若s[i] \< t[i]：

这种情况下可以将s[i]执行若干次向后切换的操作变为t[i]。方便起见，记index_s和index_t分别为s[i]和t[i]在字母表中的下标，那么这样的话代价就是

nextCost[index_s] + nextCost[index_s + 1] + ... + nextCost[index_t - 1]

除此之外，也可以执行将s[i]执行若干次向前切换的操作变为'a'，然后套个圈变为'z'，再继续执行向前切换的操作变为t[i]。其中将s[i]变为'a'再套圈变为'z'的代价为

previousCost[index_s] + previousCost[index_s - 1] + ... + previousCost[0]

再从'z'变为t[i]的代价则为

previousCost[25] + previousCost[24] + ... + previousCost[index_t + 1]

二者之和就是向前操作的代价

3、若s[i] > t[i]：

此时与情况2相反，s[i]可以执行若干次向前的操作变为t[i]，或者执行若干次向后的操作先变为'z'，然后套个圈变为'a'，再继续执行向后的操作变为t[i]。这两种操作的代价分别

previousCost[index_s] + previousCost[index_s - 1] + ... + previousCost[index_t + 1]

以及

(nextCost[index_s] + nextCost[index_s + 1] + ... + nextCost[25]) + (nextCost[0] + ... + nextCost[index_t - 1])

可以发现，上面的式子中出现了nextCost的区间和、previousCost的前缀和以及后缀和、previousCost的区间和、nextCost的后缀和以及前缀和，于是在这里可以针对nextCost和previousCost分别计算前缀和或者后缀和，就可以利用前缀和或者后缀和在O(1)的时间内得到每种操作的代价了。我在这里计算的是nextCost的前缀和以及previousCost的后缀和。

最后附上python代码：

```python
class Solution(object):
    def shiftDistance(self, s, t, nextCost, previousCost):
        """
        :type s: str
        :type t: str
        :type nextCost: List[int]
        :type previousCost: List[int]
        :rtype: int
        """
        
        next_s = [nextCost[0]]
        for v in nextCost[1:]:
            next_s.append(next_s[-1] + v)
        
        prev_s = [previousCost[-1]]
        for v in previousCost[-2::-1]:
            prev_s.append(prev_s[-1] + v)
        prev_s.reverse()

        res = 0
        for sc, tc in zip(s, t):
            if sc == tc:
                continue
            index_s = ord(sc) - 97
            index_t = ord(tc) - 97
            if index_s < index_t:
                next_cost = next_s[index_t - 1]
                if index_s > 0:
                    next_cost -= next_s[index_s - 1]

                prev_cost = prev_s[0] - prev_s[index_s + 1]
                if index_t  < 25:
                    prev_cost += prev_s[index_t + 1]
            else:
                next_cost = next_s[-1] - next_s[index_s - 1]
                if index_t > 0:
                    next_cost += next_s[index_t - 1]

                prev_cost = prev_s[index_t + 1]
                if index_s < 25:
                    prev_cost -= prev_s[index_s + 1]

            res += min(next_cost, prev_cost)
        
        return res
```
