---
title: "3316. 从原字符串里进行删除操作的最多次数"
aliases: ["yiduobo的每日leetcode 3316.从原字符串里进行删除操作的最多次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/two-pointers", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1918143761"
zhihu_id: "1918143761"
zhihu_title: "yiduobo的每日leetcode 3316.从原字符串里进行删除操作的最多次数"
question_id: "3316"
question: "从原字符串里进行删除操作的最多次数"
problem_url: "https://leetcode.cn/problems/find-maximum-removals-from-source-string/"
difficulty: "Medium"
rating: 2062
created: "2024-10-19T01:17:07+08:00"
updated: "2024-10-19T01:17:07+08:00"
upvotes: 0
comments: 0
---

# 3316. 从原字符串里进行删除操作的最多次数

> **[yiduobo的每日leetcode 3316.从原字符串里进行删除操作的最多次数](https://zhuanlan.zhihu.com/p/1918143761) · 知乎 · 2024-10-19 · 赞同 0**
> 力扣：[3316. 从原字符串里进行删除操作的最多次数](https://leetcode.cn/problems/find-maximum-removals-from-source-string/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3316.从原字符串里进行删除操作的最多次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-maximum-removals-from-source-string/description/)

题目给出一个长度为n的字符串source以及source的一个子序列pattern，另外给出一个有序的下标数组targetIndices，其中包含的是0到n - 1中互不相同的数字。

现在定义一次操作为删除source中下标在idx的一个字符，需要满足idx是targetIndices中的一个元素，且删除对应的字符后pattern任然是source的子序列。需要注意在这里执行操作并不会影响字符在source中的下标位置，例如从'acb'中删除c，下标为2的字符依然为'b'。

现在要求计算最多可以执行多少次删除操作。

乍一看没有想到比较好的贪心方案，另外从这个数据规模来看也比较适合O(n^2)的算法，于是可以想办法往动态规划上去靠。

最直观的思路就是令f[i][j]表示source的前i个字符，在满足可以从中选出子序列构成pattern的前j个字符的前提下最多可以删除的字符数量。

那么对于f[i][j]：

1、当i和j都为0时：

表示空串匹配空序列，此时有f[i][j] \= 0

2、当i为0且j > 0时：

此时由于s中没有字符，必然无法构成子序列，因此有f[i][j] \= None

3、当i > 0时：

首先初始化f[i][j]为空，因为暂时还不知道是否存在可行的构造方案。

接下来无论j等于多少，都有一种选项，就是删除掉source中的第i个字符，当然这里删除的前提是f[i - 1][j]非空。这种情况下就有f[i][j] \= f[i - 1][j] + delta，这里的delta表示是否是有效的删除，即下标i - 1是否处于targetIndices中。只有在这种情况下才有必要删除这个字符。

另外当j > 0时，也可以尝试source[i - 1]与pattern[j - 1]的匹配，若二者相等，且f[i - 1][j - 1]非空，那么也可以用f[i - 1][j - 1]来更新f[i][j]。

另外注意到f的每一轮的状态都只与上一轮有关，因此可以倒序遍历j来节省掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def maxRemovals(self, source, pattern, targetIndices):
        """
        :type source: str
        :type pattern: str
        :type targetIndices: List[int]
        :rtype: int
        """

        n = len(source)
        m = len(pattern)

        f = [None] * (m + 1)
        p = 0
        f[0] = 0
        for i in range(1, n + 1):
            while p < len(targetIndices) and targetIndices[p] < i - 1:
                p += 1
            
            if p < len(targetIndices) and targetIndices[p] == i - 1:
                delta = 1
            else:
                delta = 0

            for j in range(m, -1, -1):
                if f[j] is not None:
                    f[j] = f[j] + delta
                if j > 0 and source[i - 1] == pattern[j - 1] and f[j - 1] is not None:
                    if f[j] is None or f[j] < f[j - 1]:
                        f[j] = f[j - 1]

        return f[m]
```
