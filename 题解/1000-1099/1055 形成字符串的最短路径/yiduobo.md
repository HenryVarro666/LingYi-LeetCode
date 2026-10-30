---
title: "1055. 形成字符串的最短路径"
aliases: ["yiduobo的每日leetcode 1055.形成字符串的最短路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/607021780"
zhihu_id: "607021780"
zhihu_title: "yiduobo的每日leetcode 1055.形成字符串的最短路径"
question_id: "1055"
question: "形成字符串的最短路径"
problem_url: "https://leetcode.cn/problems/shortest-way-to-form-string/"
created: "2023-02-17T01:13:20+08:00"
updated: "2023-02-17T01:13:20+08:00"
upvotes: 0
comments: 0
---

# 1055. 形成字符串的最短路径

> **[yiduobo的每日leetcode 1055.形成字符串的最短路径](https://zhuanlan.zhihu.com/p/607021780) · 知乎 · 2023-02-17 · 赞同 0**
> 力扣：[1055. 形成字符串的最短路径](https://leetcode.cn/problems/shortest-way-to-form-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1055.形成字符串的最短路径

[力扣](https://leetcode.cn/problems/shortest-way-to-form-string/)

为了最终串联的字符串数量最少，在这里就应该尽量让target中的每一个字符向前匹配，那么可以使用一个变量p记录当前在source中匹配的起始位置，初始值为0。

接下来从头开始向后遍历target，对于当前遍历到的字符char，不断将p向后直到p来到source的末尾，或者source[p]等于char为止。若p来到了source末尾，那么将p置为0，将最终答案加上1，然后再重复执行一次这个过程。若依然没找到匹配的source[p]，那么说明char没有在source出现过，此时直接返回-1，否则就将p再向后移动一位。

重复这个过程，直到匹配完target中所有的字符为止。

注意到上面算法中的匹配过程实际上就是要求解出对于source中每个位置而言，某个字符下一次出现的下标。对于这个问题，可以先从后往前一趟遍历预处理出来。需要注意这里的下一个位置是环形的，所以需要遍历两次。

得到每个字符下一次出现的位置后，上面算法的遍历匹配char就可以变成通过这里记录的下一个位置进行跳转，从而将时间复杂度从O(mn)优化到O(26m + n)，其中m和n分别为source和target的长度。

最后附上python代码：

```python
class Solution(object):
    def shortestWay(self, source, target):
        """
        :type source: str
        :type target: str
        :rtype: int
        """

        next_pos = {}
        for index in range(len(source) -1, -1, -1):
            next_pos[source[index]] = index
        
        pos_list = []
        for index in range(len(source) - 1, -1, -1):
            next_pos[source[index]] = index
            pos_list.append(next_pos.copy())
        
        pos_list.reverse()

        p = 0
        res = 1

        for char in target:
            if char not in pos_list[p]:
                return -1
            
            if pos_list[p][char] < p:
                res += 1
            p = pos_list[p][char] + 1
            if p == len(source):
                p = 0
                res += 1
        
        if p == 0:
            res -= 1

        return res
```
