---
title: "1794. 统计距离最小的子串对个数"
aliases: ["yiduobo的每日leetcode 1794.统计距离最小的子串对个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/621496710"
zhihu_id: "621496710"
zhihu_title: "yiduobo的每日leetcode 1794.统计距离最小的子串对个数"
question_id: "1794"
question: "统计距离最小的子串对个数"
problem_url: "https://leetcode.cn/problems/count-pairs-of-equal-substrings-with-minimum-difference/"
created: "2023-04-13T00:36:59+08:00"
updated: "2023-04-13T00:36:59+08:00"
upvotes: 0
comments: 0
---

# 1794. 统计距离最小的子串对个数

> **[yiduobo的每日leetcode 1794.统计距离最小的子串对个数](https://zhuanlan.zhihu.com/p/621496710) · 知乎 · 2023-04-13 · 赞同 0**
> 力扣：[1794. 统计距离最小的子串对个数](https://leetcode.cn/problems/count-pairs-of-equal-substrings-with-minimum-difference/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1794.统计距离最小的子串对个数

[力扣](https://leetcode.cn/problems/count-pairs-of-equal-substrings-with-minimum-difference/)

题目中给出的前三个条件是常规的两个字符串中相同的子串，而最后这个条件则比较微妙。题目要求第一个子串的终点位置j减去第二个子串的起点位置a最小，那么可以明确的是最终答案的子串长度必然为1，因为对于长度大于1的两个子串s1[i : j + 1]以及s2[a : b + 1]而言，如果这两个字符串相同，那么s1[i]必然等于s2[a]，此时距离计算的方法就变成了i - a。由于字符串的长度大于1，因此必然满足i \< j，从而可知i - a \< j - a，因此最终答案对应的只能是长度为1的子串。

在确定了最终答案字符串的长度为1后，不妨设这个字符为char，那么为了使得j - a最小，就应该选择s1中char第一次出现的下标作为j，同时选择s2中char最后一次出现的下标作为a。

有了上面的结论后，就分别遍历两个字符串，记录各种字符在s1中第一次出现的下标，以及各种字符在s2中最后一次出现的下标。接下来再遍历每种字符，计算其对应的j - a，统计最小的j - a出现的次数作为最终答案。

最后附上python代码：

```python
class Solution(object):
    def countQuadruples(self, firstString, secondString):
        """
        :type firstString: str
        :type secondString: str
        :rtype: int
        """

        min_dis = 10 ** 6
        first = {}
        last = {}
        for index, char in enumerate(firstString):
            if char not in first:
                first[char] = index
        
        for index, char in enumerate(secondString):
            last[char] = index
        
        res = 0
        for char in first:
            if char in last:
                dis = first[char] - last[char]
                if dis < min_dis:
                    min_dis = dis
                    res = 1
                elif dis == min_dis:
                    res += 1
        
        return res
```
