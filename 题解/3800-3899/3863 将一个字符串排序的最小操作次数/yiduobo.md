---
title: "3863. 将一个字符串排序的最小操作次数"
aliases: ["yiduobo的每日leetcode 3863.将一个字符串排序的最小操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2014136948151834235"
zhihu_id: "2014136948151834235"
zhihu_title: "yiduobo的每日leetcode 3863.将一个字符串排序的最小操作次数"
question_id: "3863"
question: "将一个字符串排序的最小操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-sort-a-string/"
difficulty: "Medium"
rating: 1860
created: "2026-03-11T23:59:37+08:00"
updated: "2026-03-11T23:59:41+08:00"
upvotes: 1
comments: 0
---

# 3863. 将一个字符串排序的最小操作次数

> **[yiduobo的每日leetcode 3863.将一个字符串排序的最小操作次数](https://zhuanlan.zhihu.com/p/2014136948151834235) · 知乎 · 2026-03-11 · 赞同 1**
> 力扣：[3863. 将一个字符串排序的最小操作次数](https://leetcode.cn/problems/minimum-operations-to-sort-a-string/) · Medium · 灵茶山艾府：[分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3863.将一个字符串排序的最小操作次数

<https://leetcode.cn/problems/minimum-operations-to-sort-a-string/>

题目给出一个由小写英文字母组成的字符串s。

在一次操作中，可以选择s的任意子串(但不能选择整个字符串)，将其按照字母升序排序。

要求返回使得s按照升序排列所需的最小操作次数，若无法达成，则返回-1。

首先考虑无解的情况。从题目给出的样例来看，唯一无解的情况，就是s的长度恰好为2，且s[0] > s[-1]。此种情况下，因为不能选择整个字符串进行排序，也就是说无法对s进行任何操作，此时的答案就是-1。

接下来对于一般情况。

1、若s本来就是有序的：

此时无需进行任何操作，答案就是0

2、若s[0]是s中最小的字符，或者s[-1]是s中最大的字符：

对于前者，只需要将s[1:]进行排序就行了；对于后者，只需要将s[:len(s) - 1]进行排序就行了

因此，这种情况下答案就是1

3、若s[0]不是s中最小的字符，且s[-1]不是s中最大字符：

对于这种情况，理想情况下有两种方案：

- 通过一次操作让最小的字符排到s[0]，然后对s[1:]进行另一次操作让数组有序
- 通过一次操作让最大的字符排到s[-1]，然后对s[:len(s) - 1]进行另一次操作让数组有序

但是有一种特殊情况，就是s[0]是s中最大的字符，s[-1]是s中最小的字符，且s中其他的字符既不是最大的字符，也不是最小的字符。对于这种情况，无法在第一次操作中让最小或者最大的字符归位，必须先通过一次操作，让最小或者最大的字符排到中间的部位，然后再通过一次操作让最小或者最大的字符归位，再对剩余的字符串进行最后一次操作，使得数组有序。

也就是说，若s[0]是最大的字符，s[-1]是最小的字符，且s[1: len(s) - 1]中没有s中最小以及最大的字符，那么答案就是3，否则答案就是2。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        if len(s) == 2 and s[0] > s[-1]:
            return -1
        
        flag = True
        for index in range(1, len(s)):
            if s[index] < s[index - 1]:
                flag = False
                break

        if flag:
            return 0
        
        ma, mi = s[0], s[0]
        for c in s[1:]:
            if c > ma:
                ma = c
            if c < mi:
                mi = c
        
        if s[0] == mi or s[-1] == ma:
            return 1
        
        if s[0] == ma and s[-1] == mi:
            for c in s[1: len(s) - 1]:
                if c == ma or c == mi:
                    return 2
            return 3
        
        return 2
```
